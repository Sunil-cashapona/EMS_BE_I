from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    authorization_user,
    get_current_user,
    hash_password
)
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserEdit,
    UserResponse,
    UserDelete
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user_data = user.model_dump()

    password = user_data.pop("password")

    user_data["password_hash"] = hash_password(password)

    new_user = User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user




@router.get(
    "/{employee_id}",
    response_model=UserResponse
)
def get_user(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = (
        db.query(User)
        .filter(User.employee_id == employee_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user




@router.put(
    "/{employee_id}",
    response_model=UserResponse
)
def update_user(
    employee_id: str,
    user_data: UserEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = (
        db.query(User)
        .filter(User.employee_id == employee_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin cannot update user details"
        )

    if current_user.employee_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own details"
        )

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user




@router.delete(
    "/",
    status_code=status.HTTP_200_OK
)
def delete_user(
    user_data: UserDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):
    user = (
        db.query(User)
        .filter(User.employee_id == user_data.employee_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
    }

@router.patch("/{employee_id}/status")
def update_user_status(
    employee_id: str, 
    is_active:bool,
    db:Session=Depends(get_db),
    current_user: User=Depends(authorization_user)
):

    user = (
        db.query(User).filter(User.employee_id==employee_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active=is_active

    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated successfully",
        "employee_id": user.employee_id,
        "is_active": user.is_active
    }