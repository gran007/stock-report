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


def insert_company_type(id, name):
    company_type = [f for f in db_session.query(CompanyType).filter(CompanyType.id == id)]
    if len(company_type) == 0:
        db_session.add(CompanyType(id, name))


def commit():
    db_session.commit()


class DailyDataReport:
    date = ''
    code = ''
    name = ''
    closing_price = 0
    fluctuation_ratio = 0.0
    transaction_amount = 0


def select_date_and_transaction_amount(date, transaction_amount):
    company_types = {}
    for c in db_session.query(CompanyType):
        company_types[c.id] = c.name

    daily_data_date = [d[0] for d in db_session.query(DailyData)
        .with_entities(DailyData.date).distinct()
        .order_by(DailyData.date).filter(DailyData.date.startswith(date))]

    company_codes = [c[0] for c in db_session.query(DailyData.code)
        .with_entities(DailyData.code).distinct()
        .filter(DailyData.date.startswith(date),
                DailyData.transaction_amount >= transaction_amount)]

    daily_data = [d for d in db_session.query(DailyData)
        .with_entities(DailyData)
        .order_by(DailyData.code, DailyData.date)
        .filter(DailyData.code.in_(company_codes))]

    data_set = {}

    for code in company_codes:
        if code not in data_set:
            data_set[code] = {
                'name': company_types[code],
                'count': 0
            }

        for date in daily_data_date:
            items = [f for f in filter(lambda u: u.code == code and u.date == date, daily_data)]
            if len(items) > 0:
                item = items[0]
                if item.transaction_amount > transaction_amount:
                    data_set[code]['count'] += 1

                data_set[code][date] = {
                    'closing_price': item.closing_price,
                    'fluctuation_ratio': item.fluctuation_ratio,
                    'is_over_transaction_amount_standard': item.transaction_amount >= transaction_amount
                }

    return daily_data_date, sorted(data_set.items(), key=lambda s: s[0])