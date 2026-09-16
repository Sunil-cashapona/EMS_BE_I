from app.schemas.user import UserCreate, UserEdit, UserRead
from app.schemas.user_lic import UserLicCreate, UserLicEdit, UserLicRead
from app.schemas.department import DepartmentCreate, DepartmentEdit, DepartmentRead
from app.schemas.designation import DesignationCreate, DesignationEdit, DesignationRead
from app.schemas.attendence import AttendanceCreate, AttendanceEdit, AttendanceRead
from app.schemas.holiday import HolidayCreate, HolidayEdit, HolidayRead
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeEdit, LeaveTypeRead
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestEdit, LeaveRequestRead
from app.schemas.reference_type import ReferenceTypeCreate, ReferenceTypeRead
from app.schemas.reference_value import ReferenceValueCreate, ReferenceValueRead
from app.schemas.payroll_settings import (
    PayrollSettingsCreate,
    PayrollSettingsEdit,
    PayrollSettingsRead,
)
from app.schemas.salary_stucture import (
    SalaryStructureCreate,
    SalaryStructureEdit,
    SalaryStructureRead,
)
from app.schemas.salary_recod import (
    SalaryRecordCreate,
    SalaryRecordEdit,
    SalaryRecordRead,
)
from app.schemas.notification import NotificationCreate, NotificationRead
from app.schemas.user_file import UserFileRead

__all__ = [
    "UserCreate", "UserEdit", "UserRead",
    "UserLicCreate", "UserLicEdit", "UserLicRead",
    "DepartmentCreate", "DepartmentEdit", "DepartmentRead",
    "DesignationCreate", "DesignationEdit", "DesignationRead",
    "AttendanceCreate", "AttendanceEdit", "AttendanceRead",
    "HolidayCreate", "HolidayEdit", "HolidayRead",
    "LeaveTypeCreate", "LeaveTypeEdit", "LeaveTypeRead",
    "LeaveRequestCreate", "LeaveRequestEdit", "LeaveRequestRead",
    "ReferenceTypeCreate", "ReferenceTypeRead",
    "ReferenceValueCreate", "ReferenceValueRead",
    "PayrollSettingsCreate", "PayrollSettingsEdit", "PayrollSettingsRead",
    "SalaryStructureCreate", "SalaryStructureEdit", "SalaryStructureRead",
    "SalaryRecordCreate", "SalaryRecordEdit", "SalaryRecordRead",
    "NotificationCreate", "NotificationRead",
    "UserFileRead",
]