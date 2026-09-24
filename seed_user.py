from datetime import date
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import EmploymentType, Gender, Role, User

db = SessionLocal()

try:
  email = "admin@example.com"
  user = db.query(User).filter(User.email == email).first()

  if not user:
    user = User(
        employee_id="ADM001",
        first_name="System",
        last_name="Admin",
        email=email,
        password_hash=hash_password("Admin@123"),
        dob=date(1995, 1, 1),
        gender=Gender.MALE,
        phonenumber="9876543210",
        role=Role.ADMIN,
        is_active=True,
        address="Hyderabad Office",
        joining_date=date.today(),
        employment_type=EmploymentType.FULL_TIME,
        emergency_contact="9876543211",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(
        f"SUCCESS: User created with ID: {user.id} | Email: {user.email} | Role:"
        f" {user.role.value}"
    )
  else:
    print(
        f"ALREADY EXISTS: User ID: {user.id} | Email: {user.email} | Role:"
        f" {user.role.value}"
    )

except Exception as e:
  db.rollback()
  print("ERROR:", e)
finally:
  db.close()