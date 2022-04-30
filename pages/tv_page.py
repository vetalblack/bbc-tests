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

    def get_schedule(self):
        schedule_cell_locator = (By.XPATH, "//ol[@class='highlight-box-wrapper']//li")
        cell_time_locator = (By.XPATH, ".//h3[contains(@class, 'broadcast__time gamma')]")
        result = []
        for cell in self.elements_generator(schedule_cell_locator):
            self.scroll_to_element(cell)
            time_block = cell.find_element(*cell_time_locator)
            result.append(time_block.text)
        return result
