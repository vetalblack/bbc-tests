import allure
from core import BasePage
from selenium.webdriver.common.by import By


class TVPage(BasePage):
    def check_page_displaying(self):
        programmes_page_locator = (By.XPATH, "//div[contains(@class, 'programmes-page') and ./div[@id='programmes-content']]")
        with allure.step("Check displaying of programmes page"):
            assert self.find_element(programmes_page_locator, ignore_timeout=True), "Can`t find programmes page"
        with allure.step('Check displaying correct page title'):
            assert 'BBC WORLD NEWS' in self.driver.title and '- Schedules' in self.driver.title, "Incorrect page title"

    def get_schedule(self):
        schedule_cell_locator = (By.XPATH, "//ol[@class='highlight-box-wrapper']//li")
        cell_time_locator = (By.XPATH, ".//h3[contains(@class, 'broadcast__time gamma')]")
        result = []
        for cell in self.elements_generator(schedule_cell_locator):
            self.scroll_to_element(cell)
            time_block = cell.find_element(*cell_time_locator)
            result.append(time_block.text)
        return result
