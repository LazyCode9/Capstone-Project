import pytest
from api.notes_api import NotesAPI
from config.environment import config
import time


@pytest.mark.api
def test_login_api():

    notes_api = NotesAPI()

    response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert response.status_code == 200

    response_body = response.json()

    assert "token" in response_body["data"]




@pytest.mark.api
@pytest.mark.smoke
def test_create_note_api():

    notes_api = NotesAPI()

    login_response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert login_response.status_code == 200

    timestamp = int(time.time())

    title = f"API_Note_{timestamp}"
    description = f"API_Description_{timestamp}"
    category = "Home"

    response = notes_api.create_note(
        title,
        description,
        category
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True

    note_data = response_body["data"]

    assert note_data["title"] == title
    assert note_data["description"] == description
    assert note_data["category"] == category
    assert note_data["completed"] is False



@pytest.mark.api
@pytest.mark.regression
def test_delete_note_api():

    notes_api = NotesAPI()

    login_response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert login_response.status_code == 200

    timestamp = int(time.time())

    title = f"Delete_API_Note_{timestamp}"
    description = f"Delete_API_Description_{timestamp}"
    category = "Work"

    create_response = notes_api.create_note(
        title,
        description,
        category
    )

    assert create_response.status_code == 200

    create_response_body = create_response.json()

    note_id = create_response_body["data"]["id"]

    delete_response = notes_api.delete_note(
        note_id
    )

    assert delete_response.status_code == 200

    delete_response_body = delete_response.json()

    assert delete_response_body["success"] is True
    assert delete_response_body["status"] == 200

  


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_notes_api():

    notes_api = NotesAPI()

    login_response = notes_api.login(
        config.get("email"),
        config.get("password")
    )

    assert login_response.status_code == 200

    timestamp = int(time.time())

    title = f"GET_API_Note_{timestamp}"
    description = f"GET_API_Description_{timestamp}"
    category = "Personal"

    create_response = notes_api.create_note(
        title,
        description,
        category
    )

    assert create_response.status_code == 200

    response = notes_api.get_all_notes()

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True

    notes = response_body["data"]

    created_note = next(
        (
            note for note in notes
            if note["title"] == title
        ),
        None
    )

    assert created_note is not None, \
        "Created note not found in GET notes response"

    assert created_note["description"] == description
    assert created_note["category"] == category


from api.notes_api import NotesAPI

@pytest.mark.api
@pytest.mark.smoke
def test_health_check_api():

    notes_api = NotesAPI()

    response = notes_api.health_check()

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["status"] == 200
    assert response_body["message"] == "Notes API is Running"

    



@pytest.mark.api
@pytest.mark.negative
def test_login_api_invalid_password():

    notes_api = NotesAPI()

    response = notes_api.login(
        config.get("email"),
        "WrongPassword123"
    )

    assert response.status_code == 401

    response_body = response.json()

    assert response_body["success"] is False

    import pytest

from api.notes_api import NotesAPI


@pytest.mark.api
@pytest.mark.security
def test_get_notes_without_authentication():

    notes_api = NotesAPI()

    response = notes_api.get_all_notes()

    assert response.status_code == 401

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["status"] == 401

    import pytest

from api.notes_api import NotesAPI


@pytest.mark.api
@pytest.mark.security
def test_access_protected_api_without_authentication():

    notes_api = NotesAPI()

    response = notes_api.get_all_notes()

    assert response.status_code == 401

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["status"] == 401

    import pytest
import time

from api.notes_api import NotesAPI
from config.environment import config


@pytest.mark.api
@pytest.mark.negative
def test_register_with_existing_email():

    notes_api = NotesAPI()

    response = notes_api.register_user(
        name="Sujal",
        email=config.get("email"),
        password="TestPassword123"
    )

    assert response.status_code == 409

    response_body = response.json()

    assert response_body["success"] is False

    