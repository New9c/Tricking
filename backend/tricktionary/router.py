from typing import Dict
from fastapi import APIRouter, Depends

from tricktionary.schemas import TrickCreate, TrickDelete
import tricktionary.service as service
from dependencies import get_tricktionary_collection as get_collection

core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "Trick Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "Trick Not Found"},
}

router = APIRouter(
    prefix="/api/v1/tricktionary",
    tags=["Tricktionary"]
)

@router.get("/get", responses=core_responses)
def fetch_tricks(tricks_collection = Depends(get_collection)) -> dict:
    return service.fetch_tricks(tricks_collection)

@router.post("/add", responses=core_responses)
def add_trick(trick: TrickCreate, tricks_collection = Depends(get_collection)) -> dict:
    service.add_trick(trick, tricks_collection)
    return {"status_code": 200}

@router.delete("/delete/{trick}", responses=core_responses)
def delete_trick(trick: str, tricks_collection = Depends(get_collection)):
    service.delete_trick(trick, tricks_collection)
    return {"status_code": 200}
