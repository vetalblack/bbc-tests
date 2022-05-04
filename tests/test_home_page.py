import allure
import pytest
from pages.components.footer import Footer
from pages.home_page import HomePage
from pages.tv_page import TVPage


@allure.title('switch')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("parameters", [({
    'page_name': 'Home'
})])
@pytest.mark.parametrize("browser", ['chrome'])
def test_switch_footer_pages(parametrized_driver, parameters, browser):
    footer = Footer(parametrized_driver)
    home_page = HomePage(parametrized_driver)
    tv_page = TVPage(parametrized_driver)

    with allure.step('Switch to the TV page from footer'):
        footer.switch_to_page('TV')

    with allure.step('Check displaying of the TV page'):
        tv_page.check_page_displaying()

    with allure.step('Switch to the Home page from footer'):
        footer.switch_to_page('Home')

    with allure.step('Check displaying of the Home page'):
        home_page.check_page_displaying()
