from core import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, ElementNotVisibleException


class Header(BasePage):
    LOCATOR_MORE_BUTTON = (By.ID, "orb-nav-more")

    def switch_to_page(self, page_name: str):
        current_page = self.get_page_name_by_url()
        if current_page != page_name:
            try:
                button_locator = (By.XPATH, f"//div[@id='orb-header']//nav[contains(@class, 'international')]//li[.='{page_name}']")
                self.find_and_click(button_locator)
            except (ElementNotInteractableException, ElementNotVisibleException):
                button_locator = (By.XPATH, f"//ul[contains(@class, 'more-international')]//li[.='{page_name}']")
                self.find_and_click(self.LOCATOR_MORE_BUTTON)
                self.find_and_click(button_locator)

            self.wait_element_stable((By.XPATH, "//body"))
