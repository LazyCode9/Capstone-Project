import pytest
import time

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from api.notes_api import NotesAPI

from config.environment import config


@pytest.mark.e2e
@pytest.mark.regression
def test_validate_ui_to_api_note_consistency(driver):

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    

    login_page.load()

    login_page.navigate_to_login()

    login_page.login(
        config.get("email"),
        config.get("password")
    )

    timestamp = int(time.time())

    title = f"UI_API_Note_{timestamp}"
    description = f"UI_API_Description_{timestamp}"

    notes_page.click_add_note()

    notes_page.create_note(
        title,
        description
    )

    assert notes_page.is_note_created(title), \
        "Note creation failed in UI"

 

    notes_api = NotesAPI()

    login_response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert login_response.status_code == 200

    response = notes_api.get_all_notes()

    assert response.status_code == 200

    response_body = response.json()

    notes = response_body["data"]

    created_note = next(
        (
            note for note in notes
            if note["title"] == title
        ),
        None
    )

    assert created_note is not None, \
        "UI-created note not found in API response"

    assert created_note["title"] == title
    assert created_note["description"] == description

    