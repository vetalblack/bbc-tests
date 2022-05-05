import allure
import pytest
from pages.components.header import Header
from pages.home_page import HomePage
from pages.tv_page import TVPage


@allure.title('Switch between header pages')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("parameters", [({
    'page': 'Home',
    'name': 'Switch between header pages'
})])
@pytest.mark.parametrize("browser", ['chrome', 'firefox'])
def test_switch_header_pages(parametrized_driver, parameters, browser):
    header = Header(parametrized_driver)
    home_page = HomePage(parametrized_driver)
    tv_page = TVPage(parametrized_driver)

    with allure.step('Switch to the TV page from header'):
        header.switch_to_page('TV')

    with allure.step('Check displaying of the TV page'):
        tv_page.check_page_displaying()

    with allure.step('Switch to the Home page from header'):
        header.switch_to_page('Home')

    with allure.step('Check displaying of the Home page'):
        home_page.check_page_displaying()
