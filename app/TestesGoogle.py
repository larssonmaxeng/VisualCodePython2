
import numpy as np

from email.encoders import encode_base64
import json
from json import *
from urllib import response


import matplotlib.pyplot as mlt
import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl

import io

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from urllib import response
from app import googleSheet


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

        self.creds = Credentials.from_authorized_user_info(userinfo, scopes=SCOPES)     

    def GetCred(self):
        return self.creds                
    def GetDados(self, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
               
        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        return result.get('values', [])  


print("teste")
sheet = GoogleSheet()
planilha = sheet.GetDados(SAMPLE_RANGE_NAME='dados!A2:C11', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
index = sheet.GetDados(SAMPLE_RANGE_NAME='dados!A2:A11', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
colunas = sheet.GetDados(SAMPLE_RANGE_NAME='dados!A1:C1', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')

dataFrame = pd.DataFrame(planilha,index=index, columns=colunas)

