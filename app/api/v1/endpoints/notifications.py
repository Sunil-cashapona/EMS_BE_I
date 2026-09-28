from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.notification import NotificationType
from app.schemas.notification import (
    NotificationRead,
    NotificationCreate,
    NotificationListResponse,
)
from app.services.notification_service import (
    get_user_notifications,
    mark_all_notifications_as_read,
    mark_single_as_read,
    create_system_notification,
)

# ---------------------------------------------------------------------------
# Notifications Router
# Mounted at '/notifications' in app/main.py
# ---------------------------------------------------------------------------
router = APIRouter(tags=["Notifications"])


# ===========================================================================
# 1. GET /notifications
# List paginated notifications for current user with optional tab category
# ===========================================================================
@router.get("", response_model=NotificationListResponse)
def list_notifications(
    notification_type: NotificationType | None = Query(
        default=None,
        description="Tab category filter: 'leave', 'salary', 'attendance', 'general'. Omit for 'All Notifications'.",
    ),
    limit: int = Query(default=20, ge=1, le=100, description="Max notifications to return per page (1-100)"),
    offset: int = Query(default=0, ge=0, description="Number of notifications to skip for pagination"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve in-app notifications for the logged-in employee.

    - **notification_type**: Pass 'leave', 'salary', 'attendance', or 'general' to view a specific tab.
      Leave empty to get all notifications.
    - **limit & offset**: Supports infinite scroll or paginated notification lists.
    - **Response**: Contains `items` (list of notifications), `total` (count for current tab),
      and `unread_count` (global unread badge count for the header bell icon).
    """
    return get_user_notifications(
        db=db,
        current_user=current_user,
        notification_type=notification_type,
        limit=limit,
        offset=offset,
    )


# ===========================================================================
# 2. PATCH /notifications/read-all
# Mark all unread notifications of the current user as read
# ===========================================================================
@router.patch("/read-all", status_code=status.HTTP_200_OK)
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark all unread notifications for the logged-in user as read.
    Triggered when user clicks 'Mark all as read' in the notification dropdown.
    """
    count = mark_all_notifications_as_read(db=db, current_user=current_user)
    return {"message": f"{count} notifications marked as read."}


# ===========================================================================
# 3. PATCH /notifications/{notification_id}/read
# Mark a single notification as read
# ===========================================================================
@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_one_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark an individual notification as read when clicked.
    Only the owner of the notification can mark it as read.
    """
    notification = mark_single_as_read(
        db=db,
        notification_id=notification_id,
        current_user=current_user,
    )
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    return notification


# ===========================================================================
# 4. POST /notifications
# Trigger/send a notification to a specific user (System / Admin / Test)
# ===========================================================================
@router.post("", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def trigger_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Manually trigger or send a notification to a user.
    Useful for system testing or admin broadcast messages.
    """
    # Ensure the target user exists before creating the notification
    target_user = db.query(User).filter(User.id == notification_data.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target user with id {notification_data.user_id} not found",
        )

    return create_system_notification(
        db=db,
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        notification_type=notification_data.type,
    )