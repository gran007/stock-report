from model import *


def show_tables():
    queries = db_session.query(DailyData).all()
    entries = [dict(id=q.id, date=q.date, name=q.company.name) for q in queries]
    print(entries)


def delete_daily_data(date):
    db_session.query(DailyData).filter(DailyData.date == date).delete()


def insert_daily_data(date, row):
    db_session.add(DailyData(date, row))


def insert_company_type(row):
    company_type = [f for f in db_session.query(CompanyType).filter(CompanyType.id == row[0])]
    if len(company_type) == 0:
        db_session.add(CompanyType(row))


def commit():
    db_session.commit()
