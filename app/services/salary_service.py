from fastapi import HTTPException
from decimal import Decimal 
from datetime import date
from sqlalchemy.orm import Session 
from app.models.salary_record import SalaryRecord,SalaryStatus
from app.models.salary_structure import SalaryStructure
from app.models.payroll_settings import PayrollSetting, PayrollSettingType
from app.models.user import User 

def get_salary_history(db: Session, user_id : int):
    records = (db.query(SalaryRecord)
               .filter(SalaryRecord.user_id == user_id)
               .order_by(SalaryRecord.month_year.desc())
               .all())
    result = []
    for record in records:
        gross_earnings = (record.basic_salary + record.allowances)

        result.append({
            "id": record.id,
            "month_year": record.month_year,
            "payment_date": record.payment_date,
            "basic_salary": record.basic_salary,
            "gross_earnings": gross_earnings,
            "total_deductions": record.deductions,
            "net_take_home": record.net_salary,
            "status": record.status.value,
            "payslip_file": record.payslip_file
        })

    return result 

def get_current_salary_structure(
    db: Session,
    user_id: int 
):
    salary_structure = (
        db.query(SalaryStructure)
        .filter(
            SalaryStructure.user_id == user_id
        )
        .order_by(
            SalaryStructure.effective_from.desc()
        )
        .first()
    )

    if not salary_structure:
        raise HTTPException(
            status_code=404,
            detail="Salary structure not found"
        )
    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if user.salary is None:
        raise HTTPException(
            status_code=404,
            detail="Annual CTC not found"
        )
     # Annual CTC stored in txn_user.salary
    annual_ctc = user.salary

    # Convert annual CTC to monthly CTC
    monthly_ctc = annual_ctc / Decimal("12")

    # Calculate gross monthly earnings
    gross_monthly_earnings = (
        salary_structure.basic_salary
        + salary_structure.hra
        + salary_structure.other_allowances
    )

    # Get the latest salary record
    salary_record = (
        db.query(SalaryRecord)
        .filter(
            SalaryRecord.user_id == user_id
        )
        .order_by(
            SalaryRecord.month_year.desc()
        )
        .first()
    )

    gross_monthly_earnings = (
        salary_structure.basic_salary
        + salary_structure.hra
        + salary_structure.other_allowances
    )

    # If no monthly salary record exists yet,
    # deduction values are not available.
    if not salary_record:
        raise HTTPException(
            status_code=404,
            detail="Salary record not found"
        )


    return {
        "annual_ctc": annual_ctc,
        "monthly_ctc": monthly_ctc,
        "basic_salary": salary_structure.basic_salary,
        "hra": salary_structure.hra,
        "other_allowances": salary_structure.other_allowances,
        "gross_monthly_earnings": gross_monthly_earnings,
        "pf": salary_record.pf,
        "esi": salary_record.esi,
        "professional_tax": salary_record.tax,
        "lic_deductions": salary_record.lic_deductions,
        "total_deductions": salary_record.deductions,
        "net_take_home": salary_record.net_salary,
        "effective_from": salary_structure.effective_from 
    } 

def generate_salary_record(
    db: Session,
    user_id: int, 
    month_year: str
):
    # 1. Check employee
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # 2. Get current salary structure
    salary_structure = (
        db.query(SalaryStructure)
        .filter(
            SalaryStructure.user_id == user_id
        )
        .order_by(
            SalaryStructure.effective_from.desc()
        )
        .first()
    )

    if not salary_structure:
        raise HTTPException(
            status_code=404,
            detail="Salary structure not found"
        )

    # 3. Check whether salary is already generated
    existing_record = (
        db.query(SalaryRecord)
        .filter(
            SalaryRecord.user_id == user_id,
            SalaryRecord.month_year == month_year
        )
        .first()
    )

    if existing_record:
        raise HTTPException(
            status_code=400,
            detail="Salary already generated for this month"
        )

    # 4. Calculate monthly earnings
    basic_salary = salary_structure.basic_salary

    allowances = (
        salary_structure.hra
        + salary_structure.other_allowances
    )

    gross_salary = (
        basic_salary
        + allowances
    )


   # 5. Get payroll settings

    payroll_settings = (
        db.query(PayrollSetting)
        .filter(
            PayrollSetting.effective_from <= date.today()
        )
        .all()
    )

    settings = {
        setting.type: Decimal(str(setting.rate_percent))
        for setting in payroll_settings
    }

    pf_rate = settings.get(
        PayrollSettingType.PF,
        Decimal("0.00")
    )

    esi_rate = settings.get(
        PayrollSettingType.ESI,
        Decimal("0.00")
    )

    tax_rate = settings.get(
        PayrollSettingType.TAX,
        Decimal("0.00")
    )


    # 6. Calculate deductions

    # PF → calculated on basic salary
    pf = basic_salary * pf_rate / Decimal("100")

    # ESI → calculated on gross salary
    esi = gross_salary * esi_rate / Decimal("100")

    # Tax → calculated on gross salary
    tax = gross_salary * tax_rate / Decimal("100")

    # LIC is currently not automatically calculable
    # because your User model only contains lic_policy_number.
    lic_deductions = Decimal("0.00")


    total_deductions = (
        pf
        + esi
        + tax
        + lic_deductions
    )

    net_salary = gross_salary - total_deductions
    # 6. Create salary record
    salary_record = SalaryRecord(
        user_id=user_id,
        month_year=month_year,
        basic_salary=basic_salary,
        allowances=allowances,
        deductions=total_deductions,
        tax=tax,
        pf=pf,
        esi=esi,
        lic_deductions=lic_deductions,
        net_salary=net_salary,
        status=SalaryStatus.GENERATED
    )

    db.add(salary_record)
    db.commit()
    db.refresh(salary_record)

    return salary_record