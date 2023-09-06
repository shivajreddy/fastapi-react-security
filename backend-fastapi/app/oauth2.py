from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError

from app.config import settings
from app.schema import AccessTokenData, RefreshTokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: User) -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES_IN)

    access_token_payload = AccessTokenData(
        username=data.username,
        roles=data.roles,
        created_at=datetime.utcnow().isoformat(),
        exp=expire.replace(tzinfo=timezone.utc),
    )

    encoded_jwt = jwt.encode(
        access_token_payload.model_dump(),
        settings.ACCESS_TOKEN_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def create_refresh_token(data: User):
    expire = datetime.utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_IN)

    refresh_token_payload = RefreshTokenData(
        username=data.username,
        created_at=datetime.now(tz=timezone.utc).isoformat(),
        exp=expire.replace(tzinfo=timezone.utc),
    )

    encoded_jwt = jwt.encode(
        refresh_token_payload.model_dump(),
        settings.REFRESH_TOKEN_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def verify_access_token(given_token):
    try:
        payload = jwt.decode(
            given_token,
            settings.ACCESS_TOKEN_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # access_token_data = AccessTokenData(**payload)
        access_token_data = AccessTokenData(**payload)

    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access-Token's payload is not of Type AccessTokenData",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access-Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="JWTError - token is not able to decode",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return access_token_data


def verify_refresh_token(given_token) -> RefreshTokenData:
    try:
        payload = jwt.decode(
            given_token,
            settings.REFRESH_TOKEN_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        refresh_token_data = RefreshTokenData(**payload)

    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh-Token's payload is not of Type RefreshTokenData",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh-Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="JWTError - token is not able to decode",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return refresh_token_data


def get_current_user_data(token: str = Depends(oauth2_scheme)) -> AccessTokenData:
    return verify_access_token(token)
