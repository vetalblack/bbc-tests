import pytest
import os
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import constatns
from pages.components.footer import Footer


def driver_init(browser, name='auto test'):
    if constatns.REMOTE_DRIVER_IP:
        remote_url = f"http://{constatns.REMOTE_DRIVER_IP}:4444/wd/hub"
        capabilities = {
            "browserName": browser,
            # "version": "93.0",
            "enableVNC": True,
            "enableVideo": True,
            'videoName': f'{name}.mp4',
            "name": name,
            "sessionTimeout": '5m',
            "session-attempt-timeout": '5m',
            "service-startup-timeout": '5m',
            "goog:loggingPrefs": {'browser': 'ALL'}
        }
        driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=capabilities)
    else:
        if browser == 'chrome':
            driver = webdriver.Chrome(ChromeDriverManager().install())
        elif browser == 'opera':
            driver = webdriver.Opera(OperaDriverManager().install())
        elif browser == 'firefox':
            driver = webdriver.Firefox(GeckoDriverManager().install())
        else:
            raise AssertionError("Incorrect browser type")

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
def parametrized_driver(parameters: dict, browser: str):
    """
    parameters = {
        'page_name': 'TV'
    }
    """
    page_name = parameters.get('page_name')
    driver = driver_init(browser)
    driver.get(constatns.BASE_BBC_URL)
    Footer(driver).switch_to_page(page_name)

    yield driver

    driver.quit()


def attach_data(driver):
    allure.attach(
        driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )
