import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config


@pytest.fixture(scope="function")
def driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.implicitly_wait(config.get("implicit_wait"))

    yield driver

    driver.quit()