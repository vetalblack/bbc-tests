from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import constatns


def antistale(func):
    # retry function when StaleElementReferenceException appears
    def wrap(*args, **kwargs):
        count = 0
        while count < 10:
            try:
                return func(*args, **kwargs)
            except StaleElementReferenceException:
                count += 1
        return func(*args, **kwargs)
    return wrap


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10, ignore_timeout=False) -> WebElement:
        if ignore_timeout:
            try:
                element = WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located(locator))
            except TimeoutException:
                element = None
        else:
            element = WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located(locator),
                                                                message=f"Can't find element by locator {locator}")
        return element

    def elements_generator(self, locator, timeout=10):
        assert self.is_element_displayed(locator, timeout=timeout), 'Any elements is displayed on the page'
        elements = self.driver.find_elements(*locator)
        for element in elements:
            yield element

    def is_element_displayed(self, locator, timeout=10):
        try:
            self.find_element(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, webelement, to_top=False):
        top_value = 'true' if to_top else 'false'
        self.driver.execute_script(f"arguments[0].scrollIntoView(alignToTop={top_value});", webelement)

    def scroll_to_page_bottom(self):
        self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")

    def find_and_click(self, locator, timeout=10):
        element = self.find_element(locator, timeout=timeout)
        self.scroll_to_element(element)
        element.click()

    def find_and_enter(self, locator, text, time=10):
        element = self.find_element(locator, time)
        element.send_keys(text)
        return element

    def wait_element_changing(self, html, locator, time=10):
        WebDriverWait(self.driver, time).until(ElementChanged(html, locator), message=f"Element hasn`t been changed")

    def wait_element_stable(self, locator, timeout=3, retry_limit=10):
        element_html = self.get_element_html(locator)
        retry_count = 0
        while retry_count <= retry_limit:
            try:
                self.wait_element_changing(element_html, locator, time=timeout)
            except TimeoutException:
                return
            retry_count += 1
            element_html = self.get_element_html(locator)
        raise AssertionError('Webelement is not stable')

    @antistale
    def get_element_html(self, locator):
        element = self.find_element(locator)
        attribute_value = element.get_attribute('innerHTML')
        return attribute_value

    def get_page_name_by_url(self):
        current_url = self.driver.current_url
        if current_url == f"{constatns.BASE_BBC_URL}/":
            page_name = "Home"
            return page_name

        url_type = current_url.split('/')[3]
        if url_type == "schedules":
            page_name = "TV"
        else:
            page_name = url_type.capitalize()
        return page_name


class ElementChanged(object):

    # Custom waiter for WebdriverWait: wait changing element in the DOM

    def __init__(self, html, locator):
        self.html = html
        self.locator = locator

    @staticmethod
    @antistale
    def get_element_html(driver, by, value):
        element = driver.find_element(by, value)
        html = element.get_attribute('innerHTML')
        return html

    def __call__(self, driver):
        old_html = self.html
        new_html = self.get_element_html(driver, *self.locator)
        if old_html != new_html:
            return True
        else:
            return False
