import os
import allure
from utils.attach import attach_screenshot, attach_video, attach_page_dump
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selene import browser, support

import config


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": config.url_app,

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test_4",

            # Set your access credentials
            "userName": config.bstack_user_name,
            "accessKey": config.bstack_access_key
        }
    })

    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)

    browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    attach_screenshot(browser)

    attach_page_dump(browser)

    bstack_session_id = browser.driver.session_id

    with allure.step('Tear down app session'):
        browser.quit()

    attach_video(bstack_session_id)
