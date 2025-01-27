import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from dependencies import get_tricktionary_collection, mock_tricktionary_collection
from user.service import register_user  # Make sure to import your service functions

# Override the dependency in the FastAPI app
app.dependency_overrides[get_tricktionary_collection] = mock_tricktionary_collection
assert mock_tricktionary_collection().name.startswith("mock")
#Delete All
mock_tricktionary_collection().delete_many({})

client = TestClient(app)
ENCODED_HEADER = {"content-type": "application/x-www-form-urlencoded"}


def test_fetch_tricks_empty():
    response = client.get("/api/v1/tricktionary/get")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response)==mock_tricktionary_collection().count_documents({})

def test_add_trick():
    assert mock_tricktionary_collection().count_documents({"name": "Back Flip"}) == 0
    trick_data = {
        "name" : "Back Flip",
        "level" : "Novice",
        "desc" : "A god damn description."
    }
    response = client.post("/api/v1/tricktionary/add", json=trick_data)
    assert response.status_code == 200
    assert mock_tricktionary_collection().count_documents({"name": "Back Flip"}) == 1

def test_lack_desc_add_trick():
    start = mock_tricktionary_collection().count_documents({"name": "Back Flip"})
    trick_data = {
        "name" : "Back Flip",
        "level" : "Novice"
    }
    response = client.post("/api/v1/tricktionary/add", json=trick_data)
    assert response.status_code != 200
    assert mock_tricktionary_collection().count_documents({"name": "Back Flip"})==start


def test_fetch_tricks_one():
    response = client.get("/api/v1/tricktionary/get")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response)==mock_tricktionary_collection().count_documents({})


def test_delete_trick():
    assert mock_tricktionary_collection().count_documents({"name": "Back Flip"})==1
    trick_name = "Back Flip"
    response = client.delete(f"/api/v1/tricktionary/delete/{trick_name}")
    assert response.status_code == 200
    assert mock_tricktionary_collection().count_documents({"name": "Back Flip"})==0
"""
def test_fail_register_user():
    user_data = {
        "username": "test",
        "email": "test@gmail.com",
        "phone": "1234567890",
        "gender": "male",
        "age": 19,
        "password": "test"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code != 200

user_token = None
def test_login():
    global user_token
    user_data= {
        "grant_type": "password",
        "username": "test",
        "password": "test"
    }
    response = client.post("/api/v1/login", data=user_data, headers=ENCODED_HEADER)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"
    user_token = json_response["access_token"]
    assert user_token!=None

def test_no_user_login():
    user_data= {
        "grant_type": "password",
        "username": "not_in_collection",
        "password": "test"
    }
    response = client.post("/api/v1/login", data=user_data, headers=ENCODED_HEADER)
    assert response.status_code != 200

def test_incorrect_pwd_login():
    user_data= {
        "grant_type": "password",
        "username": "test",
        "password": "wrong_pwd"
    }
    response = client.post("/api/v1/login", data=user_data, headers=ENCODED_HEADER)
    assert response.status_code != 200




def test_no_header_fetch_user():
    response = client.get("/api/v1/me")
    assert response.status_code != 200


def test_bad_token_fetch_user():
    assert user_token!=None
    header = {
        "Authorization": f"Bearer BAD_TOKEN"
    }
    response = client.get("/api/v1/me", headers=header)
    assert response.status_code != 200


def test_update_user():
    assert user_token!=None
    header = {
        "Authorization": f"Bearer {user_token}"
    }

    update_data = {
        "age": 12,
        "gender": "male"
    }

    response = client.put("/api/v1/me", json=update_data, headers=header)
    assert response.status_code == 200
"""
