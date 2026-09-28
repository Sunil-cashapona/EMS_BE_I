from fastapi import HTTPException
from sqlalchemy.orm import Session 
from app.models.salary_record import SalaryRecord
from app.models.salary_structure import SalaryStructure

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

    gross_monthly_earnings = (
        salary_structure.basic_salary
        + salary_structure.hra
        + salary_structure.other_allowances
    )

    return {
        "basic_salary": salary_structure.basic_salary,
        "hra": salary_structure.hra,
        "other_allowances": salary_structure.other_allowances,
        "gross_monthly_earnings": gross_monthly_earnings,
        "effective_from": salary_structure.effective_from 
    } 