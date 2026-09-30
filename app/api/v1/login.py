from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.user import (
    LoginRequest,
    LoginResponse
)

from app.services.auth_service import (
    login_user,
    logout_user
)


router = APIRouter()

security = HTTPBearer()


# ==================================================
# LOGIN
# ==================================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    return login_user(
        login_data,
        db
    )


# ==================================================
# LOGOUT
# ==================================================

@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # Get token from:
    # Authorization: Bearer <access_token>

    token = credentials.credentials

    return logout_user(
        token=token,
        db=db
    )