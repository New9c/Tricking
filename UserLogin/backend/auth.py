from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from schemas import User
from typing import Annotated
from config import config


_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def _authenticate_user_token(token: Annotated[str, Depends(_oauth2_scheme)]):
    try:
        payload = jwt.decode(token, config.SECRET_JWT, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

CurrentLoggedInUser = Annotated[str, Depends(_authenticate_user_token)]
