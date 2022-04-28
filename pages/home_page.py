from core import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    def is_page_displayed(self):
        media_list_locator = (By.XPATH, "//ul[contains(@class, 'media-list')]")
        is_media_list_displayed = self.is_element_displayed(media_list_locator)
        page_title = self.driver.title
        if is_media_list_displayed and page_title == 'BBC - Homepage':
            return True
        else:
            return False


