from typing import Dict
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from user.auth import CurrentLoggedInUser
from user.schemas import UserCreate, UserRoleUpdate, UserUpdate
import user.service as service
from dependencies import get_users_collection as get_collection

router = APIRouter(
    prefix="/api/v1",
    tags=["User"]
)

core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "User Not Found"},
}

@router.post("/register", responses=core_responses)
def register_user(user: UserCreate, users_collection = Depends(get_collection)) -> dict:
    service.register_user(user, users_collection)
    return {"status_code": 200}

@router.post("/login", responses=core_responses)
def login(form_data: OAuth2PasswordRequestForm = Depends(), users_collection = Depends(get_collection)) -> dict:
    return service.login(form_data, users_collection)

@router.put("/me", responses=core_responses)
def update_user(username: CurrentLoggedInUser, user: UserUpdate, users_collection = Depends(get_collection)) -> dict:
    return service.update_user(username, user, users_collection)

@router.get("/me", responses=core_responses)
def fetch_user(username: CurrentLoggedInUser, users_collection = Depends(get_collection)):
    return service.fetch_user(username, users_collection)

@router.delete("/delete/{account}", responses=core_responses)
def delete_user(account: str, users_collection = Depends(get_collection)) -> dict:
    service.delete_user(account, users_collection)
    return {"status_code": 200}

@router.get("/users", responses=core_responses)
def admin_fetch_users(admin: CurrentLoggedInUser, users_collection = Depends(get_collection)) -> dict:
    return service.admin_fetch_users(admin, users_collection)

@router.post("/update_role", responses=core_responses)
def admin_update_user_role(admin: CurrentLoggedInUser, user: UserRoleUpdate,  users_collection = Depends(get_collection))-> dict:
    return service.admin_update_user_role(admin, user, users_collection)
