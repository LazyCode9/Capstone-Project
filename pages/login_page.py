from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.environment import config


class LoginPage(BasePage):

    # Locators
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='alert-message']")

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
    
    LOGIN_NAV_BUTTON = (By.XPATH, "//a[contains(text(),'Login')]")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Login')]")

    DASHBOARD_TEXT = (By.CSS_SELECTOR, "[data-testid='home']")

    # Actions
    def load(self):
        self.open_url(config.get("base_url"))

    def login(self, email, password):
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def navigate_to_login(self):
        self.click(self.LOGIN_NAV_BUTTON)
    
    def is_login_successful(self):
        return self.is_visible(self.DASHBOARD_TEXT)