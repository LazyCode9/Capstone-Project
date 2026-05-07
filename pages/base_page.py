from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.environment import config
import time


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            config.get("explicit_wait")
        )

    def open_url(self, url):
        self.driver.get(url)

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)
        element.click()

    def enter_text(self, locator, text):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.2)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element.text

    def is_visible(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element.is_displayed()