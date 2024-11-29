import os
#from google.oauth2.credentials import Credentials
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#from googleapiclient.discovery import build
import pickle
from datetime import datetime

class GoogleSheetsAPI:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = '1234567890'  # Replace with your spreadsheet ID
        self.creds = None
        self.service = None
        self.setup_credentials()

    def setup_credentials(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)

    def get_sheet_data(self, range_name):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_name
            ).execute()
            return result.get('values', [])
        except Exception as e:
            print(f"Error getting sheet data: {e}")
            return []

    def update_sheet(self, range_name, values):
        try:
            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            return result
        except Exception as e:
            print(f"Error updating sheet: {e}")
            return None

class FreelanceManager:
    def __init__(self):
        self.sheets_api = GoogleSheetsAPI()
        self.FREELANCE_RANGE = 'Frellancer!C2:G'
        self.CRM_RANGE = 'CRM Freelancer!A2:E'

    def get_freelance_projects(self):
        return self.sheets_api.get_sheet_data(self.FREELANCE_RANGE)

    def get_crm_data(self):
        return self.sheets_api.get_sheet_data(self.CRM_RANGE)

    def add_project(self, project_data):
        current_data = self.get_freelance_projects()
        new_row = [
            project_data.get('data', datetime.now().strftime('%Y-%m-%d')),
            project_data.get('tipo', ''),
            project_data.get('projeto', ''),
            project_data.get('preco', ''),
            project_data.get('status', '')
        ]
        
        next_row = len(current_data) + 2  # +2 because we start at row 2
        range_name = f'Frellancer!C{next_row}:G{next_row}'
        
        return self.sheets_api.update_sheet(range_name, [new_row])

    def update_project_status(self, row_number, new_status):
        range_name = f'Frellancer!G{row_number}'
        return self.sheets_api.update_sheet(range_name, [[new_status]])

def setup_routes(app, freelance_manager):
    @app.route('/api/projects', methods=['GET'])
    def get_projects():
        projects = freelance_manager.get_freelance_projects()
        return {'projects': projects}

    @app.route('/api/projects', methods=['POST'])
    def add_new_project():
        project_data = request.json
        result = freelance_manager.add_project(project_data)
        return {'success': bool(result), 'result': result}

    @app.route('/api/projects/<int:row>/status', methods=['PUT'])
    def update_status(row):
        new_status = request.json.get('status')
        result = freelance_manager.update_project_status(row, new_status)
        return {'success': bool(result), 'result': result}

    @app.route('/api/crm', methods=['GET'])
    def get_crm():
        crm_data = freelance_manager.get_crm_data()
        return {'crm_data': crm_data}



if __name__ == '__main__':
    pass