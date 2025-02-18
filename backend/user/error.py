from fastapi import HTTPException

USER_ALREADY_EXISTS = HTTPException(status_code=400, detail="User Already Exists")
INVALID_PARAMETERS = HTTPException(status_code=401, detail="Invalid Parameters")
PASSWORD_INVALID = HTTPException(status_code=401, detail="Password Invalid")
USER_NOT_FOUND = HTTPException(status_code=404, detail="User Not Found")
ADMIN_NOT_FOUND = HTTPException(status_code=404, detail="Admin Not Found")
NOT_ADMIN = HTTPException(status_code=403, detail="Not Admin")
