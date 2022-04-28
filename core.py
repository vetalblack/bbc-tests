from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10) -> WebElement:
        element = WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located(locator),
                                                            message=f"Can't find element by locator {locator}")
        return element

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
