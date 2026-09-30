from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User
from app.models.session import UserSession
from app.core.database import get_db


security = HTTPBearer()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 7


# --------------------------------------------------
# CREATE ACCESS TOKEN
# --------------------------------------------------

def create_access_token(
    user_id: int,
    role: str,
    sid: str
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "sid": sid,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --------------------------------------------------
# CREATE REFRESH TOKEN
# --------------------------------------------------

def create_refresh_token(
    user_id: int,
    role: str,
    sid: str
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "sid": sid,
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --------------------------------------------------
# DECODE TOKEN
# --------------------------------------------------

def decode_token(token: str) -> dict:

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )


# --------------------------------------------------
# GET CURRENT USER
# --------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Get token from:
    # Authorization: Bearer <token>

    token = credentials.credentials

    try:

        # Decode and validate JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID
        user_id = payload.get("sub")

        # Get token type
        token_type = payload.get("type")

        # Get session ID
        sid = payload.get("sid")

        # Validate user ID
        if user_id is None:
            raise credentials_exception

        # Validate session ID
        if sid is None:
            raise credentials_exception

        # Only access tokens can access protected APIs
        if token_type != "access":
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception


    # --------------------------------------------------
    # CHECK SESSION
    # --------------------------------------------------

    user_session = (
        db.query(UserSession)
        .filter(
            UserSession.session_id == sid,
            UserSession.is_active == True
        )
        .first()
    )

    if user_session is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been logged out",
            headers={"WWW-Authenticate": "Bearer"},
        )


    # --------------------------------------------------
    # FIND USER
    # --------------------------------------------------

    current_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if current_user is None:
        raise credentials_exception


    # --------------------------------------------------
    # CHECK USER ACTIVE STATUS
    # --------------------------------------------------

    if not current_user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )


    return current_user


# --------------------------------------------------
# ADMIN AUTHORIZATION
# --------------------------------------------------

def authorization_user(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Access Required"
        )

    return current_user