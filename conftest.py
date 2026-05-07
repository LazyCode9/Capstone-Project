import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config


@pytest.fixture(scope="function")
def driver():

    options = Options()

    # Disable notifications & popups
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.implicitly_wait(config.get("implicit_wait"))

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to Allure on test failure."""
    outcome = yield
    report = outcome.get_result()

    # Only act on failures during the "call" phase (i.e., the actual test)
    if report.when == "call" and report.failed:
        # Try to get the driver from the fixture
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )