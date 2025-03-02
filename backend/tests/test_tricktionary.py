import pytest
from fastapi.testclient import TestClient
from main import app
from dependencies import get_tricktionary_collection, mock_tricktionary_collection

# Override the dependency in the FastAPI app
app.dependency_overrides[get_tricktionary_collection] = mock_tricktionary_collection


mock_tricktionary_collection().delete_many({})
client = TestClient(app)


trick = {
    "name" : "Back Flip",
    "level" : "Novice",
    "desc" : "A god damn description."
}

def test_fetch_tricks_empty():
    response = client.get("/api/v1/tricktionary/get")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response)==mock_tricktionary_collection().count_documents({})

def test_add_trick():
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]}) == 0
    response = client.post("/api/v1/tricktionary/add", json=trick)
    assert response.status_code == 200
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]}) == 1

def test_add_trick_already_exists():
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]}) != 0
    response = client.post("/api/v1/tricktionary/add", json=trick)
    assert response.status_code != 200

def test_lack_desc_add_trick():
    start = mock_tricktionary_collection().count_documents({"name": trick["name"]})
    lack_desc_trick = trick.copy()
    lack_desc_trick.pop("desc")
    response = client.post("/api/v1/tricktionary/add", json=lack_desc_trick)
    assert response.status_code != 200
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]})==start


def test_fetch_tricks_one():
    response = client.get("/api/v1/tricktionary/get")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response)==mock_tricktionary_collection().count_documents({})


def test_delete_trick():
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]})==1
    response = client.delete(f"/api/v1/tricktionary/delete/{trick["name"]}")
    assert response.status_code == 200
    assert mock_tricktionary_collection().count_documents({"name": trick["name"]})==0
