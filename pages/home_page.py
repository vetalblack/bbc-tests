import allure
from core import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    def check_page_displaying(self):
        home_page_heading = (By.XPATH, "//section[contains(@class, 'module module--header')]//h2//span[.='Welcome to BBC.com']")
        with allure.step('Check displaying of page heading'):
            assert self.find_element(home_page_heading, ignore_timeout=True), "Can`t find heading on the page"
        with allure.step('Check displaying correct page title'):
            assert self.driver.title == 'BBC - Homepage', "Incorrect page title"
