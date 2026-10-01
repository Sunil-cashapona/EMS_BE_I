from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session
from app.models.salary_record import SalaryRecord 

def get_salary_payroll_report(db: Session,
    month_year: str | None = None,):
    
    query = db.query(SalaryRecord)

    if month_year:
        query = query.filter(
            SalaryRecord.month_year == month_year
        )

    records = query.order_by(
        SalaryRecord.month_year.desc(),
        SalaryRecord.user_id
    ).all()

    report_records = []

    total_disbursed_net = Decimal("0.00")
    pf_deductions_collected = Decimal("0.00")
    lic_premiums_remitted = Decimal("0.00")

    for record in records:

        gross_salary = (
            record.basic_salary
            + record.allowances
        )

        total_deductions = (
            record.tax
            + record.pf
            + record.esi
            + record.lic_deductions
        )

        employee_name = ""

        if record.user:
            employee_name = (
                f"{record.user.first_name} "
                f"{record.user.last_name}"
            ).strip()

        report_records.append(
            {
                "month_year": record.month_year,
                "employee_id": record.user_id,
                "employee_name": employee_name,
                "basic_salary": record.basic_salary,
                "gross_salary": gross_salary,
                "deductions": total_deductions,
                "net_disbursed": record.net_salary,
            }
        )

        total_disbursed_net += record.net_salary
        pf_deductions_collected += record.pf
        lic_premiums_remitted += record.lic_deductions 

    return {
        "generated_date": date.today().isoformat(),
        "summary": {
            "total_disbursed_net": total_disbursed_net,
            "pf_deductions_collected": pf_deductions_collected,
            "lic_premiums_remitted": lic_premiums_remitted,
        },
        "records": report_records,
    }