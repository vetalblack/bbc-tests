from core import BasePage
from selenium.webdriver.common.by import By


class Footer(BasePage):
    def switch_to_page(self, page_name: str):
        button_locator = (By.XPATH, f"(//div[@id='orb-footer']//div[contains(@class, 'orb-footer-primary-links')]//ul[contains(@class, 'international')]//li[.='{page_name}'])[last()]")
        self.find_and_click(button_locator)
        self.wait_element_stable((By.XPATH, "//body"))
