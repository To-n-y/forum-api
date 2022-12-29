from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from models import connect_db, AuthToken


def check_auth_token(token: str, database=Depends(connect_db)):
    token = database.query(AuthToken).filter(AuthToken.token == token).one_or_none()
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect token'
        )
    return token
