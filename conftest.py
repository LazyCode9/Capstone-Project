import pytest
import allure

from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config


@pytest.fixture(scope="function")
def driver():

    options = Options()

    # -----------------------------
    # Chrome Preferences
    # -----------------------------
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
    }

    options.add_experimental_option("prefs", prefs)

    # -----------------------------
    # Chrome Arguments
    # -----------------------------
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    # Recommended for Docker/Grid
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    # # Optional Headless Mode
    if config.get("headless"):
        options.add_argument("--headless=new")

    execution = config.get("execution")

    # -----------------------------
    # Local Execution
    # -----------------------------
    if execution == "local":

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    # -----------------------------
    # Selenium Grid Execution
    # -----------------------------
    elif execution == "remote":

        driver = webdriver.Remote(
            command_executor=config.get("grid_url"),
            options=options
        )

    else:
        raise ValueError(
            f"Invalid execution type: {execution}"
        )

    driver.implicitly_wait(config.get("implicit_wait"))

    yield driver

    driver.quit()


# =========================================
# Capture Screenshot on Failure
# =========================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Only capture failures during test execution
    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            screenshot = driver.get_screenshot_as_png()

            allure.attach(
                screenshot,
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )