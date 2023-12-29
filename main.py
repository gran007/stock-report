import openpyxl
import os
import glob
from db_manager import *

path = 'C:\\Users\\gran007\\Desktop\\주식\\202311'


def insert_excel_data():
    company_info = {}

    for file_path in glob.glob(f'{path}/*.xlsx'):
        basename = os.path.basename(file_path)
        date = os.path.splitext(basename)[0]
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        delete_daily_data(date)
        for row in [r for r in ws.rows][1:]:
            row_data = [c.value for c in row]
            company_info[row_data[0]] = row_data[1]
            insert_daily_data(date, row_data)
        commit()

    for id, name in company_info.items():
        insert_company_type(id, name)
    commit()


if __name__ == '__main__':
    insert_excel_data()
