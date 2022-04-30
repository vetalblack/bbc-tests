from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


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

    def find_element(self, locator, timeout=10) -> WebElement:
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

    def find_and_click(self, locator, timeout=10):
        element = self.find_element(locator, timeout=timeout)
        element.click()

    def find_and_enter(self, locator, text, time=10):
        element = self.find_element(locator, time)
        element.send_keys(text)
        return element

    def wait_element_changing(self, html, locator, time=10):
        WebDriverWait(self.driver, time).until(ElementChanged(html, locator), message=f"Element hasn`t been changed")

    def wait_element_stable(self, locator, timeout=2, retry_limit=10):
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
