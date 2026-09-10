from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import LoginRequest
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)


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

    # Verify password
    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check whether user is active
    if hasattr(user, "is_active") and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Get role directly from txn_user
    role = user.role

    # If role is an Enum, get its value
    if hasattr(role, "value"):
        role = role.value

    # Create JWT tokens
    access_token = create_access_token(
        user_id=user.id,
        role=role
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
        role=role
    )

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": role
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }