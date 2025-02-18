from fastapi import HTTPException

TRICK_ALREADY_EXISTS = HTTPException(status_code=400, detail="Trick Already Exists")
TRICK_NOT_FOUND = HTTPException(status_code=404, detail="Trick Not Found")
