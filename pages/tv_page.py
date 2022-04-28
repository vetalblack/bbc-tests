from core import BasePage
from selenium.webdriver.common.by import By


class TVPage(BasePage):
    def is_page_displayed(self):
        programmes_page_locator = (By.XPATH, "//div[contains(@class, 'programmes-page') and ./div[@id='programmes-content']]")
        is_programmes_page_displayed = self.is_element_displayed(programmes_page_locator)
        page_title = self.driver.title
        if 'BBC WORLD NEWS' in page_title and '- Schedules' in page_title:
            is_title_correct = True
        else:
            is_title_correct = False
        if is_programmes_page_displayed and is_title_correct:
            return True
        else:
            return False
