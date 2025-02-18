from contextlib import redirect_stderr

from appium.webdriver.common.appiumby import AppiumBy
import allure
from selene import browser, have


def test_search_appium():
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with allure.step('Verify content found'):
        results = browser.all((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title"))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_search_selenium_and_click():
    search_string = 'Selenium (software)'
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type(search_string)

    with allure.step('Verify content found'):
        results = browser.all((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title"))
        results.should(have.size_greater_than(0))

    with allure.step('Verify content found'):
        results.first.should(have.text(search_string)).click()
