from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from urllib import response
class GoogleSheet:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        #GOOGLE_PRIVATE_KEY = os.environ["GOOGLE_PRIVATE_KEY"]
        # The environment variable has escaped newlines, so remove the extra backslash
        #GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')
    
        userinfo = {"token": "ya29.a0AVA9y1s37amqY4vOCU1CdRCYTZmbV6BaIospkvKPB0IMtkr3xj3exRL9kWfWH2CmD4cYktb3wTOmTuWJTOZangmfEWa5t_P8Iik53k7JVUgsX7-kcaWggUlVnq722GGxbdZ-Gj1dO_GBGveXXjF-ZS6fi3braCgYKATASAQASFQE65dr8oEFIn1f5L-23jaILO7sncA0163",
             "refresh_token": "1//0hT3WgOcvdDlJCgYIARAAGBESNwF-L9IrQuP22CnHojgrG8cvcTpJU3nU2_dkqEagDLIErEW4qtjwnpRKYuGSnirdwDoEvdkhyso", 
             "token_uri": "https://oauth2.googleapis.com/token",
             "client_id": "761690673690-1ckp1g2ebioho5tblgmnq4shm3e6famv.apps.googleusercontent.com", 
             "client_secret": "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"}
#"""token": "ya29.a0AVA9y1vZ2txmN4CeOcj4rYE3Y1nnK6LzXSpKC-UAohJY-3_0eIXK_zc9KZyL4O8h8SmOcZNTQ5CzRtDUAIbnAnF1Ggpb18fFdl_lO-kuKjMYNrDKJHwjYaZaiDKI03KK8VWGuYdwFvk45TwqF-XrNX06BJ71aCgYKATASAQASFQE65dr8MBUECD9O0afkc9eh03QZLg0163", 
#           "refresh_token": "1//0hQA7roQTrKz4CgYIARAAGBESNwF-L9Ir-MIaA7wbGx8yrD6N9FaQLMnyNvDEC6rmZWODCHKdtQNrSnPk5bQ0La1rBPSB3cZJO5U", 
#           "client_id": "578028065855-1o253ugkvql2bs75t6esudbmmh1dc8tm.apps.googleusercontent.com",
#          "client_secret": "zuHee4R9UNoRZIcZywq1yclT"
#        }    """ 
    
        self.creds = Credentials.from_authorized_user_info(userinfo, scopes=SCOPES)     
        """account_info = {
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        }

        credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)

        

        # The ID and range of a sample spreadsheet.
        self.SAMPLE_SPREADSHEET_ID = '1cInywmFgXbO4_DJv9kn-1U1pQD36O9CnSb8Lud0oUYI'
        self.SAMPLE_RANGE_NAME = 'Página1!A2:A5'

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        #print(send_from_directory('reports', path))
        #if os.path.exists('token.json'):
        self.creds = Credentials.from_authorized_user_file('/static/token.json', SCOPES)    

        # If modifying these scopes, delete the file token.json.

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())"""
    def GetCred(self):
        return self.creds                
    def GetDados(self, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
               
        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        return result.get('values', [])  
    def GetService(self):
        service = build('sheets', 'v4', credentials=self.creds)
        return service.spreadsheets()

"""   def inseriSheet(numeroLinhaInicial, numeroLinhaFinal, planilha):
          linhasNovas = []
            linhasNovas.append([numeroLinhaInicial, "teste"+str(numeroLinhaFinal)])
            linhasNovas.append([numeroLinhaInicial, "teste"+str(numeroLinhaFinal)])
            linhasNovas.append([numeroLinhaInicial, "teste"+str(numeroLinhaFinal)])
            # Call the Sheets API
            result = planilha.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range='A' + str(numeroLinhaInicial) + ':B' + str(numeroLinhaFinal),
                                            valueInputOption="RAW",
                                            body={"values": linhasNovas}).execute()
        return result.get('values', [])                                 
numeroLinhaInicial = 1
numeroLinhaFinal = 3
inseriSheet(numeroLinhaInicial, numeroLinhaFinal, sheet)
numeroLinhaInicial = 4
numeroLinhaFinal = 6
inseriSheet(numeroLinhaInicial, numeroLinhaFinal, sheet)
numeroLinhaInicial = 7
numeroLinhaFinal = 9
inseriSheet(numeroLinhaInicial, numeroLinhaFinal, sheet)
numeroLinhaInicial = 10
numeroLinhaFinal = 12
inseriSheet(numeroLinhaInicial, numeroLinhaFinal, sheet)

"""