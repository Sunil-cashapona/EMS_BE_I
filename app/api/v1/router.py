from fastapi import APIRouter
from app.api.v1 import login

from app.api.v1.endpoints import (
    users,
    departments,
    designations,
    holidays,
    leave_types,
    leave_requests,
    attendance,
    reference,
    payroll_settings,
    payroll,
    notifications,
    files,
    user_lic

)

api_router = APIRouter()

# Auth & Users
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Organization & Staff Setup
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(designations.router, prefix="/designations", tags=["designations"])
api_router.include_router(reference.router, prefix="/references", tags=["references"])

# Leaves & Attendance
api_router.include_router(holidays.router, prefix="/holidays", tags=["holidays"])
api_router.include_router(leave_types.router, prefix="/leave-types", tags=["leave-types"])
api_router.include_router(leave_requests.router, prefix="/leave-requests", tags=["leave-requests"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])

# Payroll
api_router.include_router(payroll_settings.router, prefix="/payroll-settings", tags=["payroll-settings"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])

# Utility & Documents
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(files.router, prefix="/files", tags=["files"])


api_router.include_router(user_lic.router, prefix="/user-lic", tags=["user-lic"])