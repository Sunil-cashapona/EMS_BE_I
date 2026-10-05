from fastapi import FastAPI
import app.models

from app.api.v1.login import router as login_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.attendance import router as attendance_router
from app.api.v1.endpoints.dropdown import router as dropdown_router
from app.api.v1.endpoints.leave import router as leave_router
from app.api.v1.endpoints.notifications import router as notifications_router  # <--- 1. IMPORT
from app.api.v1.endpoints.reports import router as report_router
from app.api.v1.endpoints.salary import router as salary_router
from app.api.v1.endpoints.directory import router as directory_router
from app.api.v1.endpoints.holiday import router as holiday_router

app = FastAPI(title="Employee Management System", version="0.1.0")

# Register your routers
app.include_router(login_router)
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
app.include_router(dropdown_router, prefix="/dropdown", tags=["Dropdown"])
app.include_router(leave_router)
app.include_router(notifications_router, prefix="/notifications")  # <--- Added
app.include_router(report_router)
app.include_router(directory_router)
app.include_router(salary_router)  
app.include_router(holiday_router)
### --- [NEW / ADDED: Workspace Dashboard Router] ---
from app.api.v1.endpoints.workspace import router as workspace_router

app.include_router(workspace_router)
### --- [END NEW / ADDED] ---