from types import SimpleNamespace
import pytest
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.core.security import get_current_user, security
from app.main import app


ADMIN_HEADERS = {"Authorization": "Bearer admin-test-token"}
EMPLOYEE_HEADERS = {"Authorization": "Bearer employee-test-token"}


def mock_get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    if token == "admin-test-token":
        return SimpleNamespace(id=1, email="admin@test.com", role="admin")
    elif token == "employee-test-token":
        return SimpleNamespace(id=2, email="employee@test.com", role="employee")
    raise HTTPException(status_code=401, detail="Invalid token")


@pytest.fixture(scope="session", autouse=True)
def setup_auth_override():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(scope="session")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_headers():
    return ADMIN_HEADERS


@pytest.fixture
def employee_headers():
    return EMPLOYEE_HEADERS
