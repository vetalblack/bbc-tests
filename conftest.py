import pytest
import os
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import constatns


def driver_init():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(0, 0)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


# Test fail screenshot fixture
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                for fixturename in item.fixturenames:
                    if 'driver' in fixturename:
                        web_driver = item.funcargs[fixturename]
                        web_driver.is_test_failed = True
                        attach_data(web_driver)
                        return
                print('Fail to take screen-shot')
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))


@pytest.fixture()
def parametrized_driver(parameters: dict):
    """
    parameters = {
        'page_name': 'TV'
    }
    """
    page_name = parameters.get('page_name')
    driver = driver_init()
    driver.get(constatns.BASE_BBC_URL)

    yield driver

    driver.quit()


def attach_data(driver):
    allure.attach(
        driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )
