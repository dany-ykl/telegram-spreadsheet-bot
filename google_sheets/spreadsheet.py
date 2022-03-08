import os

import gspread
from gspread import exceptions
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


template_data = {'A1': 'доп.информация',
                 'A2': 'id записи',
                 'B2': 'дата въезда',
                 'C2': 'дата выезда',
                 'D2': 'имя арендатора',
                 'E2': 'телефон',
                 'F2': 'сумма'
                }

worksheet_template = pd.DataFrame(template_data, index=[0]).values.tolist()


class GoogleSheet:

    def __init__(self, email):
        self.email = email
        self.sheetname = f'flat_{email}'
        self.client = self.get_client()

    def get_credentials(self):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive']
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        creds = os.path.join(BASE_DIR, 'credentials.json')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)
        return credentials

    def get_client(self):
        client = gspread.authorize(self.get_credentials())
        return client

    def grant_permission_owner(self, sheet_id):
        self.client.insert_permission(sheet_id,
                                      self.email,
                                      perm_type='user',
                                      role='owner')

    def get_sheet(self):
        sheet = self.client.open(self.sheetname)
        return sheet

    def exists_sheet(self):
        try:
            sheet = self.get_sheet()
            return sheet
        except:
            return False

    def create_worksheet(self, tablename, add_info=None):
        sheet = self.exists_sheet()        
        if sheet:
            sheet.add_worksheet(title=tablename, cols=1000, rows=1000)
            worksheet = sheet.worksheet(tablename)
            self.fill_worksheet(worksheet, add_info)
            return {'sheet':sheet, 'worksheet':worksheet}
        else:
            self.client.create(self.sheetname)
            sheet = self.get_sheet()
            self.grant_permission_owner(sheet_id=sheet.id)
            worksheet = sheet.get_worksheet(0)
            worksheet.update_title(tablename)
            self.fill_worksheet(worksheet=worksheet, add_info=add_info)
            return {'sheet':sheet, 'worksheet':worksheet}

    def fill_worksheet(self, worksheet, add_info=None):
        """Fills a worksheet base data"""
        worksheet.update('B1', add_info)
        worksheet.update('A1', 'доп.информация')
        worksheet.update('A2', 'id записи')
        worksheet.update('B2', 'дата въезда')
        worksheet.update('C2', 'дата выезда')
        worksheet.update('D2', 'имя арендатора')
        worksheet.update('E2', 'телефон')
        worksheet.update('F2', 'сумма')

    def get_all_worksheet(self):
        worksheet_list = self.get_sheet().worksheets()
        return worksheet_list    

    def get_worksheet(self, tablename):
        worksheet = self.get_sheet().worksheet(tablename)
        return worksheet
        
    def delete_worksheet(self, tablename):
        worksheet = self.get_worksheet(tablename)
        self.get_sheet().del_worksheet(worksheet)

    def create_entry(self, entry):
        worksheet = self.get_worksheet(entry.tablename)
        num_cell = len(worksheet.get_all_values())+1
        worksheet.update(f'A{num_cell}', entry.entry_id)
        worksheet.update(f'B{num_cell}', entry.date_entry)
        worksheet.update(f'C{num_cell}', entry.date_exit)
        worksheet.update(f'D{num_cell}', entry.name_renter)
        worksheet.update(f'E{num_cell}', entry.phone)
        worksheet.update(f'F{num_cell}', entry.amount)

    def delete_entry(self, entry):
        worksheet = self.get_worksheet(entry.tablename)
        cell = worksheet.find(entry.entry_id)
        worksheet.delete_row(cell.row)

    def get_entries(self, tablename):
        worksheet = self.get_worksheet(tablename)
        entries = worksheet.get_all_values()
        result = ''
        data = []
        for entry in entries[2:]:
            data_entry = {}
            data_entry['id'] = entry[0]
            data_entry['date_entry'] = entry[1]
            data_entry['date_exit'] = entry[2]
            data_entry['name_renter'] = entry[3]
            data_entry['phone'] = entry[4]
            data_entry['amount'] = entry[5]    
            data.append(data_entry) 

        for entry in data:
            for key, value in entry.items():
                result += key + ": " + value + ' '
            result += '\n\n'
        return result

    

