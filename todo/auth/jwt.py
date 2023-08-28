import jwt
from jwt import PyJWKError, InvalidSignatureError, DecodeError

from todo_app.models import CustomUser
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta
from ninja.security import HttpBearer

from configs import settings
from auth.schemas import TokenPayload


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


def get_current_user(token: str):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWKError:
        return None
    except InvalidSignatureError:
        return None
    except DecodeError:
        return None
    
    user = get_object_or_404(CustomUser, id=token_data.user_id)
    return user
    


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        if token:
            user = get_current_user(token)
            if user:
                return user
        
       