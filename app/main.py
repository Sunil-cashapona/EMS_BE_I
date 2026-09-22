from fastapi import FastAPI

# Import directly from the correct nested endpoints folder
from app.api.v1.login import router as login_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.attendance import router as attendance_router
from app.api.v1.endpoints.dropdown import router as dropdown_router

app = FastAPI(title="Employee Management System", version="0.1.0")

# Register your routers
app.include_router(login_router)
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
app.include_router(dropdown_router, prefix="/dropdown", tags=["Dropdown"])