import pytest
import time

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from api.notes_api import NotesAPI

from config.environment import config


@pytest.mark.e2e
@pytest.mark.regression
def test_validate_api_deletion_reflected_in_ui(driver):

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # ---------------------------------
    # UI FLOW
    # ---------------------------------

    login_page.load()

    login_page.navigate_to_login()

    login_page.login(
        config.get("email"),
        config.get("password")
    )

    timestamp = int(time.time())

    title = f"Delete_UI_API_{timestamp}"
    description = f"Delete_Description_{timestamp}"

    notes_page.click_add_note()

    notes_page.create_note(
        title,
        description
    )

    assert notes_page.is_note_created(title), \
        "Note creation failed in UI"

    # ---------------------------------
    # API FLOW
    # ---------------------------------

    notes_api = NotesAPI()

    login_response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert login_response.status_code == 200

    get_notes_response = notes_api.get_all_notes()

    notes = get_notes_response.json()["data"]

    created_note = next(
        (
            note for note in notes
            if note["title"] == title
        ),
        None
    )

    assert created_note is not None, \
        "Created note not found in API"

    note_id = created_note["id"]

    delete_response = notes_api.delete_note(
        note_id
    )

    assert delete_response.status_code == 200

    # ---------------------------------
    # REFRESH UI
    # ---------------------------------

    driver.refresh()

    assert notes_page.is_note_deleted(title), \
        "Deleted API note still visible in UI"