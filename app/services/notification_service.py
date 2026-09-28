from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.notification import Notification, NotificationType
from app.models.user import User
from app.core.timezone import get_current_localized_time


# ===========================================================================
# 1. Fetch User Notifications (with Tab Filtering & Pagination)
# ===========================================================================
def get_user_notifications(
    db: Session,
    current_user: User,
    notification_type: NotificationType | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """
    Fetch a paginated list of notifications for the currently logged-in user.

    Parameters:
    - db: Database session.
    - current_user: The authenticated user requesting their notifications.
    - notification_type: Optional tab filter (e.g. 'leave', 'salary', 'attendance', 'general').
                         If None, fetches notifications across all tabs ('All Notifications').
    - limit: Maximum number of notifications to return in one page (default 50).
    - offset: Number of notifications to skip for pagination (default 0).

    Returns:
    - items: List of Notification ORM objects ordered newest first.
    - total: Total number of notifications matching the selected tab filter (for pagination).
    - unread_count: Total unread notifications across ALL tabs (for the bell icon badge).
    """
    # Base query: Strictly isolate notifications to the logged-in user for security
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    count_query = db.query(func.count(Notification.id)).filter(Notification.user_id == current_user.id)

    # Apply category/tab filter if specified (e.g. User clicked "Leave" or "Salary" tab)
    if notification_type is not None:
        query = query.filter(Notification.type == notification_type)
        count_query = count_query.filter(Notification.type == notification_type)

    # Total matching records for this tab (used by the frontend to compute page numbers)
    total = count_query.scalar() or 0

    # Retrieve paginated items, newest first
    notifications = (
        query.order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Unread badge count: Count unread across ALL tabs so the header bell badge is always accurate
    unread_count = (
        db.query(func.count(Notification.id))
        .filter(Notification.user_id == current_user.id, Notification.is_read == False)
        .scalar()
        or 0
    )

    return {
        "items": notifications,
        "total": total,
        "unread_count": unread_count,
    }


# ===========================================================================
# 2. Mark All Notifications as Read
# ===========================================================================
def mark_all_notifications_as_read(db: Session, current_user: User) -> int:
    """
    Bulk update all unread notifications for the logged-in user to 'is_read = True'.

    Uses a direct SQL UPDATE via SQLAlchemy with synchronize_session=False
    for maximum performance (avoids loading every notification into memory).

    Returns:
    - Number of notification records that were updated.
    """
    updated = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id, Notification.is_read == False)
        .update({Notification.is_read: True}, synchronize_session=False)
    )
    db.commit()
    return updated


# ===========================================================================
# 3. Mark a Single Notification as Read
# ===========================================================================
def mark_single_as_read(db: Session, notification_id: int, current_user: User) -> Notification | None:
    """
    Mark an individual notification as read when clicked by the user.

    Ensures security by checking both:
    1. Notification.id == notification_id
    2. Notification.user_id == current_user.id (prevents unauthorized users from modifying others' items)

    Returns:
    - Updated Notification object if found, or None if not found / not owned by the user.
    """
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification


# ===========================================================================
# 4. Create a System / Triggered Notification
# ===========================================================================
def create_system_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: NotificationType,
) -> Notification:
    """
    Utility function called across the application (e.g. Leave apply/approve,
    Payroll generation, Attendance alerts) to dispatch an in-app notification.

    Parameters:
    - db: Active database session.
    - user_id: Target employee's user ID.
    - title: Notification title (e.g. 'Leave Request Approved').
    - message: Descriptive message body.
    - notification_type: Notification category ('leave', 'salary', 'attendance', 'general').

    Returns:
    - The created and committed Notification ORM object.
    """
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
        is_read=False,
        created_at=get_current_localized_time(),
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification