from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait

class NotesPage(BasePage):

    # ---------- Locators ----------

    # Add Note Button
    ADD_NOTE_BUTTON = (By.XPATH, "//button[@data-testid='add-new-note']")

    # Modal Fields
    TITLE_INPUT = (By.XPATH, "//input[@data-testid='note-title']")
    DESCRIPTION_INPUT = (By.XPATH, "//textarea[@data-testid='note-description']")
    CREATE_BUTTON = (By.XPATH, "//button[@data-testid='note-submit']")

    # Validation Messages (field-relative)
    TITLE_ERROR = (
    By.XPATH,
    "//input[@data-testid='note-title']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    DESCRIPTION_ERROR = (
    By.XPATH,
    "//textarea[@data-testid='note-description']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    # Note Card (Dynamic)
    def note_title(self, title):
        return (
            By.XPATH,
            f"//div[@data-testid='note-card-title'][text()='{title}']"
        )

    # ---------- Actions ----------

    def click_add_note(self):
        self.click(self.ADD_NOTE_BUTTON)

    def enter_title(self, title):
        self.enter_text(self.TITLE_INPUT, title)

    def enter_description(self, description):
        self.enter_text(self.DESCRIPTION_INPUT, description)

    def click_create(self):
        self.click(self.CREATE_BUTTON)

    def create_note(self, title, description):
        self.enter_title(title)
        self.enter_description(description)
        self.click_create()

    # ---------- Validations ----------

    def is_note_created(self, title):
        return self.is_visible(self.note_title(title))

    def get_title_error(self):
        return self.get_text(self.TITLE_ERROR)

    def get_description_error(self):
        return self.get_text(self.DESCRIPTION_ERROR)
    
      # Delete confirmation modal
    MODAL = (By.CSS_SELECTOR, ".modal-content")
    MODAL_CONFIRM_BTN = (By.CSS_SELECTOR, "[data-testid='note-delete-confirm']")
    MODAL_BODY = (By.CSS_SELECTOR, ".modal-content .modal-body")

    # --- Note card elements ---
    NOTE_CARD = (By.CSS_SELECTOR, "[data-testid='note-card']")
    NOTE_TITLE = (By.CSS_SELECTOR, "[data-testid='note-card-title']")
    NOTE_DELETE_BTN = (By.CSS_SELECTOR, "[data-testid='note-delete']")
    NOTE_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='toggle-note-switch']")

    def delete_note_by_title(self, title):
        """Click the Delete button for a specific note (by its title)."""
        xpath = f"//div[@data-testid='note-card' and contains(., '{title}')]//button[@data-testid='note-delete']"
        self.click((By.XPATH, xpath))

    def confirm_delete(self):
        """Click the red Delete/Confirm button in the modal."""
        self.click(self.MODAL_CONFIRM_BTN)

    def is_modal_displayed(self):
        """Check if the confirmation modal is visible."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.MODAL)
            )
            return True
        except:
            return False

    def wait_modal_closed(self):
        """Wait until the modal disappears from the DOM."""
        self.wait.until_not(EC.presence_of_element_located(self.MODAL))

    def get_note_checkbox(self, title):
        """
        Return the checkbox element of the note with the given title.
        The checkbox is inside the same card as the title.
        """
        card_xpath = f"//div[@data-testid='note-card' and contains(., '{title}')]"
        card = self.driver.find_element(By.XPATH, card_xpath)
        return card.find_element(By.CSS_SELECTOR, "[data-testid='toggle-note-switch']")

    def is_note_completed(self, title):
        """Return True if the note's checkbox is checked."""
        checkbox = self.get_note_checkbox(title)
        return checkbox.is_selected()   # 'checked' attribute present
    
    MODAL_CANCEL_BTN = (By.CSS_SELECTOR, "[data-testid='note-delete-cancel-2']")

    def cancel_delete(self):
        """Click the Cancel button inside the modal to abort deletion."""
        self.wait.until(EC.element_to_be_clickable(self.MODAL_CANCEL_BTN))
        self.click(self.MODAL_CANCEL_BTN)

    def is_note_present(self, title):
        """Check if a note card with the exact title exists in the DOM."""
        xpath = f"//div[@data-testid='note-card']//div[@data-testid='note-card-title' and normalize-space()='{title}']"
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False
        
    # Inside class NotesPage(BasePage):

    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='logout']")

    def click_logout(self):
        """Click the Logout button (assumed visible when logged in)."""
        self.click(self.LOGOUT_BUTTON)

    def note_description(self, description):
        return (
            By.XPATH,
            f"//p[@data-testid='note-card-description'][contains(text(),'{description}')]"
        )
    
    def is_note_deleted(self, title):

        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(
                    d.find_elements(*self.note_title(title))
                ) == 0
            )

            return True

        except:
            return False