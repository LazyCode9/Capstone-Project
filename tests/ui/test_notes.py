from time import time
import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
import time

@pytest.mark.ui
@pytest.mark.smoke
def test_create_note_valid(driver):

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # Login
    login_page.load()
    login_page.navigate_to_login()
    login_page.login(
        config.get("email"),
        config.get("password")
    )

    # Create Note
    title = "Capstone"
    description = "Automation Note"

    notes_page.click_add_note()
    notes_page.create_note(title, description)

    # Validation
    assert notes_page.is_note_created(title), "Note creation failed"


@pytest.mark.ui
@pytest.mark.regression
def test_create_note_empty_fields(driver):

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # Login
    login_page.load()
    login_page.navigate_to_login()
    login_page.login(
        config.get("email"),
        config.get("password")
    )

    # Open modal
    notes_page.click_add_note()

    # Click create without data
    notes_page.click_create()

    # Capture validation
    title_error = notes_page.get_title_error()
    desc_error = notes_page.get_description_error()

    # Assertions
    assert "required" in title_error.lower(), "Title validation missing"
    assert "required" in desc_error.lower(), "Description validation missing"


import time
import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config

@pytest.mark.ui
def test_delete_note_with_confirmation(driver):
    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    login_page.load()
    login_page.navigate_to_login()
    login_page.login(config.get("email"), config.get("password"))

    title = f"DelTest_{int(time.time())}"
    description = "To be deleted"
    notes_page.click_add_note()
    notes_page.create_note(title, description)
    assert notes_page.is_note_created(title), "Note creation failed"

    notes_page.delete_note_by_title(title)
    assert notes_page.is_modal_displayed(), "Modal missing"
    notes_page.confirm_delete()
    notes_page.wait_modal_closed()

    assert not notes_page.is_note_present(title), \
        f"Note '{title}' still present after deletion"
    
@pytest.mark.ui
@pytest.mark.regression
def test_cancel_note_deletion(driver):
    """
    TC-014: Cancel note deletion.
    1. Login and create a fresh note
    2. Click Delete → confirmation popup appears
    3. Click Cancel (do not confirm)
    4. Verify the note remains unchanged (not completed, still visible)
    """
    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 1. Login
    login_page.load()
    login_page.navigate_to_login()
    login_page.login(
        config.get("email"),
        config.get("password")
    )

    # 2. Create a new note (unique)
    title = f"CancelTest_{int(time.time())}"
    description = "Note for cancel delete test"

    notes_page.click_add_note()
    notes_page.create_note(title, description)
    assert notes_page.is_note_created(title), "Note creation failed"

    # 3. Initiate deletion
    notes_page.delete_note_by_title(title)

    # 4. Verify modal is displayed
    assert notes_page.is_modal_displayed(), "Delete confirmation modal did not appear"

    # 5. Click Cancel
    notes_page.cancel_delete()

    # 6. Wait for modal to close
    notes_page.wait_modal_closed()

    # 7. Assert the note is still present and NOT completed
    assert notes_page.is_note_present(title), (
        f"Note '{title}' disappeared after cancellation (should remain)"
    )
    assert not notes_page.is_note_completed(title), (
        f"Note '{title}' was incorrectly marked as completed after cancellation"
    )

@pytest.mark.ui
@pytest.mark.regression
def test_logout(driver):
    """
    TC-015: Logout from application.
    1. Login
    2. Click Logout button
    3. Assert the Login navigation button is visible (logged‑out state)
    4. Click it to reach the login form
    5. Assert the login form (email input) is displayed
    """
    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 1. Login
    login_page.load()
    login_page.navigate_to_login()
    login_page.login(
        config.get("email"),
        config.get("password")
    )

    # 2. Click Logout
    notes_page.click_logout()

    # 3. Verify the Login navigation button is visible (wait a moment)
    assert login_page.is_visible(LoginPage.LOGIN_NAV_BUTTON), \
        "Logout failed – Login navigation button not visible"

    # 4. Navigate to the actual login page (click the button)
    login_page.navigate_to_login()

    # 5. Ensure the email input field is now visible
    assert login_page.is_visible(LoginPage.EMAIL_INPUT), \
        "Login page email input not displayed after clicking Login button"