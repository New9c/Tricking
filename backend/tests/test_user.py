import unittest
from fastapi.testclient import TestClient
from main import app
from dependencies import get_users_collection, mock_users_collection

# Override the dependency in the FastAPI app
app.dependency_overrides[get_users_collection] = mock_users_collection
assert mock_users_collection().name.startswith("mock")
#Delete All
mock_users_collection().delete_many({})

client = TestClient(app)
ENCODED_HEADER = {"content-type": "application/x-www-form-urlencoded"}

def test_register_user():
    user_data = {
      "username": "test",
      "email": "test@gmail.com",
      "phone": "1234567890",
      "gender": "male",
      "age": 19,
      "password": "test"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code == 200

def test_same_register_user():
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


def test_bad_username_register_user():
    user_data = {
        "username": "has two@problems",
        "email": "no@symbol.com",
        "phone": "119110113",
        "gender": "male",
        "age": 19,
        "password": "test"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code != 200
    
def test_bad_email_register_user():
    user_data = {
        "username": "unique_user",
        "email": "no_at_symbol",
        "phone": "119110113",
        "gender": "male",
        "age": 19,
        "password": "test"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code != 200

def test_bad_age_register_user():
    user_data = {
        "username": "unique_user",
        "email": "no@symbol.com",
        "phone": "119110113",
        "gender": "male",
        "age": 3000,
        "password": "test"
    }
    response = client.post("/api/v1/register", json=user_data)
    assert response.status_code != 200

user_token: str = ""

def test_fetch_user_no_token():
    assert user_token==""
    header = {
        "Authorization": f"Bearer {user_token}"
    }
    response = client.get("/api/v1/me", headers=header)
    assert response.status_code != 200

def test_login():
    global user_token
    user_data = {
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
    assert user_token!=""

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


def test_fetch_user():
    assert user_token!=""
    header = {
        "Authorization": f"Bearer {user_token}"
    }
    response = client.get("/api/v1/me", headers=header)
    assert response.status_code == 200
    json_response = response.json()
    infos = ["username", "email", "phone", "gender", "age", "password"] 
    for info in infos:
        assert info in json_response


def test_no_header_fetch_user():
    response = client.get("/api/v1/me")
    assert response.status_code != 200


def test_bad_token_fetch_user():
    assert user_token!=""
    header = {
        "Authorization": f"Bearer BAD_TOKEN"
    }
    response = client.get("/api/v1/me", headers=header)
    assert response.status_code != 200


def test_update_user():
    assert user_token!=""
    header = {
        "Authorization": f"Bearer {user_token}"
    }

    update_data = {
        "age": 12,
        "gender": "male"
    }

    response = client.put("/api/v1/me", json=update_data, headers=header)
    assert response.status_code == 200

def test_admin_fetch_user():
    assert user_token!=""
    header = {
        "Authorization": f"Bearer {user_token}"
    }
    response = client.get("/api/v1/users", headers=header)
    assert response.status_code == 200
