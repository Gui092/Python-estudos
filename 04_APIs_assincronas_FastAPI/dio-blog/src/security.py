import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET = "my-super-secret-key-with-at-least-32-bytes"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str


def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": user_id,
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}


async def decode_jwt(token: str) -> AccessToken | None:
    try:
        decoded_token = jwt.decode(
            token,
            SECRET,
            audience="curso-fastapi",
            algorithms=[ALGORITHM],
        )

        token_data = AccessToken(**decoded_token)

        if token_data.exp < time.time():
            return None

        return token_data

    except Exception:
        return None


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> AccessToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code."
            )

        if scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme."
            )

        payload = await decode_jwt(credentials)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token."
            )

        return payload


async def get_current_user(
    token: Annotated[AccessToken, Depends(JWTBearer())]
) -> dict[str, int]:
    return {"user_id": token.sub}


def login_required(
    current_user: Annotated[dict[str, int], Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return current_user
