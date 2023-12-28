import openpyxl
import os
import glob
from db_manager import *

path = 'C:\\Users\\gran007\\Desktop\\주식\\202312'

if __name__ == '__main__':
    for file_path in glob.glob(f'{path}/*.xlsx'):
        basename = os.path.basename(file_path)
        date = os.path.splitext(basename)[0]
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        delete_daily_data(date)

        for row in [r for r in ws.rows][1:]:
            row_data = [c.value for c in row]
            insert_company_type(row_data)
            insert_daily_data(date, row_data)
        commit()
