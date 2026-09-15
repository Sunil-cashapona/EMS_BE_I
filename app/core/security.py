from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.models.user import User
from app.core.database import get_db
from fastapi import Response

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# JWT configuration
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm 

ACCESS_TOKEN_EXPIRE_MINUTES = 120 
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(user_id: int, role: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(user_id: int, role: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,SECRET_KEY,
        algorithms=[ALGORITHM]
    )

def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token=request.cookies.get("access_token")

    if token is None:
        raise credentials_exception
    
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id=payload.get("sub")

        if user_id is None:
            raise credentials_exception
        user_id=int(user_id)
        
    except (JWTError,ValueError):
        raise credentials_exception   
    
    current_user=db.query(User).filter(User.id==user_id).first()

    if current_user is None:
        raise credentials_exception
    
    return current_user






def authorization_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role !="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Access Required",
        )
    return current_user