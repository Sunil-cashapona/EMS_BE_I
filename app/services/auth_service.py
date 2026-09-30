from datetime import datetime, timedelta, timezone
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.models.user import User
from app.models.session import UserSession
from app.schemas.user import LoginRequest

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    ALGORITHM
)


# ==================================================
# LOGIN
# ==================================================

def login_user(login_data: LoginRequest, db: Session):

    # Find user
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    # User doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check whether user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Verify password
    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Get role
    role = user.role

    # If role is Enum, get its value
    if hasattr(role, "value"):
        role = role.value

    # --------------------------------------------------
    # Generate unique session ID
    # --------------------------------------------------

    sid = str(uuid.uuid4())

    # --------------------------------------------------
    # Create access token
    # --------------------------------------------------

    access_token = create_access_token(
        user_id=user.id,
        role=role,
        sid=sid
    )

    # --------------------------------------------------
    # Create refresh token
    # --------------------------------------------------

    refresh_token = create_refresh_token(
        user_id=user.id,
        role=role,
        sid=sid
    )

    # --------------------------------------------------
    # Create session record
    # --------------------------------------------------

    user_session = UserSession(
        user_id=user.id,
        session_id=sid,
        is_active=True,
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
    )

    db.add(user_session)

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user session"
        )

    # --------------------------------------------------
    # Return login response
    # --------------------------------------------------

    return {
        "user": {
            "id": user.id,
            "name": " ".join(
                part
                for part in (user.first_name, user.last_name)
                if part
            ),
            "email": user.email,
            "role": role
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ==================================================
# LOGOUT
# ==================================================

def logout_user(
    token: str,
    db: Session
):

    try:

        # Decode access token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get session ID
        sid = payload.get("sid")

        # Get token type
        token_type = payload.get("type")

        # Validate session ID
        if sid is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Logout must use access token
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token required"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # --------------------------------------------------
    # Find active session
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
            detail="Session already logged out"
        )

    # --------------------------------------------------
    # Deactivate session
    # --------------------------------------------------

    user_session.is_active = False

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not logout user"
        )

    return {
        "message": "Logged out successfully"
    }