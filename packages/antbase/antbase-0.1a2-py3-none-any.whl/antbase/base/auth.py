import os, json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import logging_v2

from pymongo import MongoClient
from aiogram import Bot, Dispatcher
from basecampy3 import Basecamp3

class Auth:
    
    # Basecamp3 ------------------------------------------------------------------
    __BC_CLIENT_               = "640f78dc4c6dda87662358c5c7c14ac3289db94c"
    __BC_CLIENT_SECRET         = "08422a5e6ab21aca66e8f5f50e79b6ba3c51d7bd"
    __BC_REDIRECT_URI          = "https://jart.jewelry/basecamp"
    __BC_ACCOUNT_ID            = "734464152727"
    __BC_REFRESH_TOKEN         = "1d8b1b4b7"

    @staticmethod
    def get_bc_client():
        return Basecamp3(
            client_id      = Auth.__BC_CLIENT_,
            client_secret  = Auth.__BC_CLIENT_SECRET,
            redirect_uri   = Auth.__BC_REDIRECT_URI,
            account_id     = Auth.__BC_ACCOUNT_ID,
            refresh_token  = Auth.__BC_REFRESH_TOKEN
        )


    # Telegram ------------------------------------------------------------------
    __TG_BOT_TOKEN             = '7877850829:AAHKFCwIEnI9MiJOmtEv1ZYx-OiKLqyVrEM'

    @staticmethod
    def get_tg_bot():
        bot = Bot(token=Auth.__TG_BOT_TOKEN)
        dp  = Dispatcher()
        return bot, dp


    # MongoDB ------------------------------------------------------------------
    __DB_TOKEN_PATH            = '/Users/dg/projects/.auth/db_token.json'
    
    @staticmethod
    def get_db_client():
        token_path = Auth.__DB_TOKEN_PATH
        if os.path.exists(token_path):
             with open(token_path, 'r') as t:
                data      = json.load(t)
                cluster   = data.get('cluster',   None)
                username  = data.get('username',  None)
                password  = data.get('password',  None)
                if cluster and username and password:
                    uri = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority"
                    client = MongoClient(uri)
                    client.admin.command('ping') # Проверка подключения
                    return client
                else:
                    raise Exception("Db Error (No cluster or apikey in token file)")


    # Google Cloud Platform ------------------------------------------------------------------
    __PROJECT_NUMBER           = 734464152727
    __PROJECT_ID               = 'antbase-435906'
    __PROJECT_NAME             = f"projects/{__PROJECT_ID}"
    __ANTHILL_NAME             = "antbase"
    __SCRIPT_ID                = "16Uveie7ijrz7b6mpCpXudxMkTJD6fhIOCVEf8PVyeDbLPnZbWlvQx1nU"
    __HEAD_DEPLOYMENT_ID       = "AKfycbxm7U9nL062DFkGvketlHNeSgbnvdyTGQiNGEvcpg0"
    __DEPLOYMENT_ID            = "AKfycbxFvTiPTdiBX9TPUd_kIVMpynt74N0HV_wvafJ-w3scK00FU9kSkyExjLx7zd_B9N-q"
    
    __CLIENT_ID                = "734464152727-5gk4pa7gd2l66mje0s6rhq97vogittkv.apps.googleusercontent.com"
    __CLIENT_SECRET_FILE       = '/Users/dg/projects/.auth/client_secret.json'
    __SERVICE_ACCOUNT_KEY      = '/Users/dg/projects/.auth/service_account_key.json'

    __GAS_TOKEN_PATH           = '/Users/dg/projects/.auth/gas_token.json'
    __DRIVE_TOKEN_PATH         = '/Users/dg/projects/.auth/drive_token.json'
    __SHEETS_TOKEN_PATH        = '/Users/dg/projects/.auth/sheets_token.json'
    __PROFILE_TOKEN_PATH       = '/Users/dg/projects/.auth/profile_token.json'
    __EMAIL_TOKEN_PATH         = '/Users/dg/projects/.auth/email_token.json'

    __LOGGING_SCOPE            = ['https://www.googleapis.com/auth/logging.admin']
    __GAS_SCOPE                = ['https://www.googleapis.com/auth/script.projects',
                                  'https://www.googleapis.com/auth/script.external_request',
                                  'https://www.googleapis.com/auth/script.scriptapp',
                                  'https://www.googleapis.com/auth/spreadsheets',
                                  'https://www.googleapis.com/auth/drive',
                                  'https://www.googleapis.com/auth/userinfo.profile',
                                  'https://www.googleapis.com/auth/userinfo.email',
                                  'openid']
    __DRIVE_SCOPE              = ['https://www.googleapis.com/auth/drive']
    __SHEETS_SCOPE             = ['https://www.googleapis.com/auth/spreadsheets']
    __PROFILE_SCOPE            = ['https://www.googleapis.com/auth/userinfo.profile',
                                  'openid']
    __EMAIL_SCOPE              = ['https://www.googleapis.com/auth/userinfo.email',
                                  'https://www.googleapis.com/auth/script.send_mail',
                                  'openid']

    @staticmethod
    def get_project_name():         return Auth.__PROJECT_NAME
    
    @staticmethod
    def get_anthill_name():         return Auth.__ANTHILL_NAME

    @staticmethod
    def get_script_id():            return Auth.__SCRIPT_ID
    
    @staticmethod
    def get_deployment_id():        return Auth.__DEPLOYMENT_ID

    @staticmethod
    def get_head_deployment_id():   return Auth.__HEAD_DEPLOYMENT_ID
                
    @staticmethod
    def get_logging_client():  # Gets credentials and builds a logging client object             
        token = service_account.Credentials.from_service_account_file(
            Auth.__SERVICE_ACCOUNT_KEY,
            scopes=Auth.__LOGGING_SCOPE)
        return logging_v2.Client(project=Auth.__PROJECT_ID, credentials=token)
    
    @staticmethod
    def get_script_service(): # Gets credentials and builds an Script service object
        '''Получает учетные данные и создает объект сервиса Google Apps Script'''
        token = Auth.__get_token(Auth.__GAS_TOKEN_PATH, Auth.__GAS_SCOPE)
        return build('script', 'v1', credentials=token)

    @staticmethod
    def get_drive_service(): # Gets credentials and builds a Drive service object
        token = Auth.__get_token(Auth.__DRIVE_TOKEN_PATH, Auth.__DRIVE_SCOPE)
        return build('drive', 'v3', credentials=token)

    @staticmethod
    def get_sheet_service(): # Gets credentials and builds a Sheets service object
        token = Auth.__get_token(Auth.__SHEETS_TOKEN_PATH, Auth.__SHEETS_SCOPE)
        return build('sheets', 'v4', credentials=token)

    @staticmethod
    def get_profile_service(): # Gets credentials and builds a Profile service object
        token = Auth.__get_token(Auth.__PROFILE_TOKEN_PATH, Auth.__PROFILE_SCOPE)
        return build('oauth2', 'v2', credentials=token)

    @staticmethod
    def get_email_service(): # Gets credentials and builds an Email service object
        token = Auth.__get_token(Auth.__EMAIL_TOKEN_PATH, Auth.__EMAIL_SCOPE)
        return build('gmail', 'v1', credentials=token)
    


    @staticmethod
    def __get_token(token_path, scope):
        token = None
        if os.path.exists(token_path):
            token = Credentials.from_authorized_user_file(token_path, scope)
        
        if not token or not token.valid:
            if token and token.expired and token.refresh_token:
                token.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(Auth.__CLIENT_SECRET_FILE, scope)
                token = flow.run_local_server(port=0)
            
            if token and token.valid:
                with open(token_path, 'w') as t:
                    t.write(token.to_json()) # Save the token for the next run
        return token