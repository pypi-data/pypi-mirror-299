#  Copyright 2023 Reid Swanson.
#
#  This file is part of scrachy.
#
#  scrachy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  scrachy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with scrachy.  If not, see <https://www.gnu.org/licenses/>.

"""
Some utility classes for sending messages between the
:class:`~scrachy.middleware.selenium.AsyncSeleniumMiddleware` and the
:mod:`~scrachy.cli.webdriver_server`. It also includes the primary
functionality for processing requests with Selenium. Each Selenium middleware
is a thin wrapper around these functions.
"""

from __future__ import annotations

# Python Modules
import logging
import time

from typing import Any, Optional, Type, cast

# 3rd Party Modules
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, HtmlResponse
from scrapy.utils.misc import load_object
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Project Modules
from scrachy.http_ import SeleniumRequest
from scrachy.settings.defaults.selenium import WebDriverName


log = logging.getLogger(__name__)


webdriver_import_base = 'selenium.webdriver'


class BufferIncompleteError(Exception):
    """Raised when the amount of data received is less than expected."""
    def __init__(self, *args):
        super().__init__(*args)


class ShutdownRequest:
    """A message token indicates the webdriver server should terminate."""
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnknownMessageType:
    """
    A message token indicates the webdriver server received an unknown message
    type.
    """
    def __init__(self, message_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message_type = message_type


class UnhandledError:
    """
    A message token indicates that an unhandled exception was raised during the
    processing of a ``SeleniumRequest``.
    """
    def __init__(self, exception: Exception, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exception = exception


def initialize_driver(
        driver_name: WebDriverName,
        options: list[str],
        extensions: list[str],
        preferences: Optional[dict[str, Any]] = None,
        page_load_timeout: Optional[float] = None,
        implicit_wait: Optional[float] = None,
        verify_proxy: bool = False
) -> WebDriver:
    """
    Construct a new webdriver instance with the given options and extensions.

    :param page_load_timeout:
    :param preferences:
    :param driver_name: The class name of the webdriver to construct.
    :param options: The list of options for the webdriver to use.
    :param extensions: The list of extensions to install.
    :param implicit_wait: The amount of time to implicitly wait.
    :param verify_proxy: If ``True`` check that the IP address of a request
           from the host machine is not the same as a request from the
           webdriver (if using a proxy).

    :return: The webdriver.
    """
    driver_name: WebDriverName = driver_name
    driver_cls: Type[WebDriver] = load_object(f'{webdriver_import_base}.{driver_name}')
    driver_options: ArgOptions = load_object(f'{webdriver_import_base}.{driver_name}Options')()

    proxy = None
    for option in options:
        if option.startswith("--proxy-server=") and driver_name == "Firefox":
            proxy_server, proxy_port = option.replace("--proxy-server=", "").split(":")
            driver_options.set_preference("network.proxy.type", 1)  # noqa
            driver_options.set_preference("network.proxy.http", proxy_server)  # noqa
            driver_options.set_preference("network.proxy.http_port", int(proxy_port))  # noqa
            driver_options.set_preference("network.proxy.ssl", proxy_server)  # noqa
            driver_options.set_preference("network.proxy.ssl_port", int(proxy_port))  # noqa
        elif not option.startswith("--class="):
            log.debug(f"Adding option '{option}' to the WebDriver.")
            driver_options.add_argument(option)
        else:
            log.warning(
                f"The --class option is reserved for use by Scrachy to help clean up "
                f"rogue processes that are not terminated by `driver.quit()`."
            )

    if preferences and driver_name == "Firefox":
        for preference_name, value in preferences.items():
            driver_options.set_preference(preference_name, value)  # noqa
    else:
        driver_options.add_experimental_option("prefs", preferences)  # noqa
    if "chrom" in driver_name.lower():
        driver_options.add_argument("--class=selenium")

    # Chrome loads the extensions from the options
    if driver_name == 'Chrome' and extensions:
        driver_options = cast(ChromiumOptions, driver_options)
        for extension in extensions:
            driver_options.add_extension(extension)  # noqa

    driver = driver_cls(options=driver_options)

    # Firefox appears to load the extension directly from the driver
    if driver_name == 'Firefox' and extensions:
        for extension in extensions:
            driver = cast(webdriver.Firefox, driver)
            driver.install_addon(extension, temporary=True)

    # implicitly_wait applies to all find element calls.
    # set_page_load_timeout applies to 'get' and 'navigate' calls.
    if page_load_timeout is not None:
        driver.set_page_load_timeout(page_load_timeout)

    if implicit_wait is not None:
        driver.implicitly_wait(implicit_wait)

    if verify_proxy:
        my_ip = _get_local_ip()
        driver_ip = _get_driver_ip(driver)

        log.debug(f"local_ip: {my_ip}, proxy_ip: {driver_ip}")
        if my_ip == driver_ip:
            raise ValueError("The local IP address is the same as the driver IP address")

    return driver


def process_request(driver: WebDriver, request: Request) -> Optional[HtmlResponse | Request]:
    if not isinstance(request, SeleniumRequest):
        # Let some other downloader handle this request
        return None

    request = cast(SeleniumRequest, request)

    try:
        driver.get(request.url)
        set_cookies(driver, request)
    except TimeoutException:
        raise WebDriverException("Failed to get the request because of a page load timeout.")
        # request.retries += 1
        # if request.retries > request.max_retries:
        #     log.error(
        #         f"The request for {request.url} reached the maximum number of retries and "
        #         f"could not be processed."
        #     )
        #     raise IgnoreRequest()
        #
        #
        #
        #
        # # Don't increase the wait time on each retry
        # page_load_timeout = driver.timeouts.page_load
        # sleep_time = page_load_timeout
        # log.warning(
        #     f"The request {request} reached the page_load_timeout of {page_load_timeout}s. "
        #     f"Sleeping for {sleep_time}s and then rescheduling the request "
        #     f"({request.retries} out of {request.max_retries})."
        # )
        #
        # time.sleep(sleep_time)
        #
        # request.dont_filter = True
        # return request

    try:
        wait_for_page(driver, request)
    except TimeoutException:
        # The timeout could actually be from a page timeout (i.e., from the
        # call to `driver.get`) or from a WebDriverWait condition (i.e.,
        # a call to `wait_for_page`). It doesn't really matter, but log
        # message will be incorrect for a page timeout.
        request.retries += 1
        if request.retries > request.max_retries:
            log.error(
                f"The request for {request.url} reached the maximum number of retries and "
                f"could not be processed."
            )
            raise IgnoreRequest()

        # Sleep longer and longer each time we time out
        sleep_time = request.wait_timeout * request.retries

        log.warning(
            f"The page for request {request} did not load properly after {request.wait_timeout} "
            f"seconds. Sleeping for {sleep_time}s and then rescheduling the request "
            f"({request.retries} out of {request.max_retries})."
        )

        time.sleep(sleep_time)

        request.dont_filter = True
        return request

    take_screenshot(driver, request)

    execute_script(driver, request)

    response = make_response(driver, request)

    return response


def set_cookies(driver: WebDriver, request: SeleniumRequest):
    for cookie_name, cookie_value in request.cookies.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})


def wait_for_page(driver: WebDriver, request: SeleniumRequest):
    if request.wait_until:
        try:
            WebDriverWait(
                driver,
                request.wait_timeout,
                poll_frequency=request.poll_frequency
            ).until(
                request.wait_until
            )
        except TimeoutException as e:
            log.error(f"Wait condition timed out for url: '{request.url}'")
            raise e


def take_screenshot(driver: WebDriver, request: SeleniumRequest):
    if request.screenshot:
        request.meta['screenshot'] = driver.get_screenshot_as_png()


def make_response(driver: WebDriver, request: SeleniumRequest) -> HtmlResponse:
    return HtmlResponse(
        url=driver.current_url,
        body=driver.page_source,
        encoding='utf-8',
        request=request,
        flags=["selenium"],
    )


def execute_script(driver: WebDriver, request: SeleniumRequest):
    if request.script_executor is not None:
        request.meta['script_result'] = request.script_executor(driver, request)


def _get_local_ip() -> str:
    import requests

    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']


def _get_driver_ip(driver: WebDriver) -> str:
    import json
    driver.get('https://api.ipify.org?format=json')
    data = driver.find_element(By.CSS_SELECTOR, 'body')
    return json.loads(data.text)['ip']
