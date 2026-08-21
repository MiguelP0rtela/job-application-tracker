from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from secrets import token_urlsafe
from app.core.config import settings
from app.database.database import get_db
from app.models.user import User
from datetime import datetime, timedelta, timezone

password_hash = PasswordHash.recommended()


########################################
############## Passwords ###############
########################################

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


########################################
################# JWT ##################
########################################

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_refresh_token() -> str:
    return token_urlsafe(64)


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user


def require_admin(
        current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )

    return current_user


def validate_password(cls, value: str) -> str:
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one number.")

    if not any(not char.isalnum() for char in value):
        raise ValueError("Password must contain at least one special character.")

    if any(char.isspace() for char in value):
        raise ValueError("Password must not contain spaces.")

    return value
