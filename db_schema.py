from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from termcolor import colored, cprint
import logging
import os
from flask import Flask, request
# import eng_class
# import amh_class
from pathlib import Path
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
############ TESTING GROUND ##################
app_creds = {
    "type": "service_account",
    "project_id": "Your Project ID",
    "private_key_id": "YOUR_PRIVATE_KEY_ID",
    "private_key": "YOUR PRIVATE KEY",
    "client_email": "YOUR_CLIENT_EMAIL",
    "client_id": "YOUR_CLIENT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "YOUR_CERT_URL"
}
# ALL of the above is in your client secrets.json file you get from Google


class User_db_update:
    def __init__(self):
        # self.chat_id = chat_id
        self.scope = ["https://spreadsheets.google.com/feeds",
                      "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file",
                      "https://www.googleapis.com/auth/drive"]

        # Your Spreadsheet id
        self.SPREADSHEET_ID = '1tgzbWndoxv-N7I7G-r4TtUfmK5zhPp83uvdnBZ8w2PM'
        self.DATA_TO_PULL = 'Data'
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(
            app_creds, self.scope)
        self.service = build('sheets', 'v4', credentials=self.creds,
                             cache_discovery=False)

    def pull_sheet_data(self, SCOPES, SPREADSHEET_ID, DATA_TO_PULL):

        # service = build('sheets', 'v4', credentials=self.creds,
        #                 cache_discovery=False)
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=DATA_TO_PULL).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                      range=DATA_TO_PULL).execute()
            data = rows.get('values')
            print("COMPLETE: Data copied")
            return data

    def update_db(self, chat_id, chat_lang, phone, password, user_id, is_registered, is_loggedin, p_plat_json, last_login, login_expiry):
        print("Updating user database ...")

        data_upd = [[str(chat_id), str(chat_lang), str(phone), str(password), str(
            user_id), str(is_registered), str(is_loggedin), str(p_plat_json), last_login, login_expiry]]

        data_new = [[str(chat_id), str(chat_lang), str(phone), str(password), str(
                    user_id), str(is_registered), str(is_loggedin), str(p_plat_json), last_login, login_expiry]]
        print(colored(chat_id, "red"))
        values_upd = data_upd
        body_upd = {'values': values_upd}
        values_new = data_new
        body_new = {'values': values_new}
        cell_lookup = User_db_checker()
        cell_lookup_row = cell_lookup.cell_lookup(str(chat_id))
        print(cell_lookup_row)
        try:
            if str(cell_lookup_row) == "None":
                result = self.service.spreadsheets().values().append(
                    spreadsheetId=self.SPREADSHEET_ID, range='Data',
                    valueInputOption="USER_ENTERED", body=body_new).execute()
                print('{0} cells appended.'.format(result
                                                   .get('updates')
                                                   .get('updatedCells')))

            else:
                my_range = str(cell_lookup_row)
                print("pass")
                result = self.service.spreadsheets().values().update(
                    spreadsheetId=self.SPREADSHEET_ID, range=my_range,
                    valueInputOption="RAW", body=body_upd).execute()
                print('{0} cells appended.'.format(result
                                                   .get('updates')
                                                   .get('updatedCells')))
        except Exception as e:
            print("Fail")


class User_db_checker:
    def __init__(self):
        # self.chat_id = chat_id
        self.scope = ["https://spreadsheets.google.com/feeds",
                      "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file",
                      "https://www.googleapis.com/auth/drive"]

        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(
            app_creds, self.scope)
        self.gc = gspread.authorize(self.creds)
        self.sh = self.gc.open("HS_bot")

        # Get all values
        self.wks_dt = self.sh.worksheet("Data")
        self.dt = self.wks_dt.get_all_values()
        self.current_data = self.wks_dt.get_all_records()
        self.headers_dt = self.dt.pop(0)
        self.df = pd.DataFrame(self.dt, columns=self.headers_dt)
        self.result = ""
        self.chat_lang = ""
        self.is_loggedin = 0
        self.is_registered = 0
        self.phone = 0
        self.password = ""
        self.last_login = ""
        self.login_expiry = ""

    def get_user(self, chat_id):
        result = ""
        chat_lang = ""
        is_loggedin = 0
        is_registered = 0
        phone = 0
        password = ""
        last_login = ""
        login_expiry = ""

        try:
            df_user = self.df.loc[self.df['chat_id']
                                  == str(chat_id)].reset_index()
            if len(df_user) == 1:
                print("User Exists in DB states!")
                chat_lang = str(df_user['chat_lang'][0])
                is_loggedin = int(str(df_user['is_loggedin'][0]))
                is_registered = int(str(df_user['is_registered'][0]))
                phone = str(df_user['phone'][0])
                password = str(df_user['password'][0])
                last_login = str(df_user['last_login'][0])
                login_expiry = str(df_user['login_expiry'][0])
                result = "Pass"

            elif len(df_user) == 0:
                result = "Fail"
                chat_lang = ""
                is_loggedin = 0
                is_registered = 0
                phone = 0
                password = ""
                last_login = ""
                login_expiry = ""

        except Exception as e:
            print(str(e) + " --- User Doesnt exist in DB States!")
            result = "Fail"
            chat_lang = ""
            is_loggedin = 0
            is_registered = 0
            phone = 0
            password = ""
            last_login = ""
            login_expiry = ""

        return result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry

    def check_lang(self, chat_id):
        chat_lang = ""
        try:
            chat_l = self.df.loc[self.df['chat_id']
                                 == str(chat_id)].reset_index()
            chat_lang = chat_l['chat_lang'][0]
        except Exception as e:
            print("no chat lang in db")
            chat_lang = "None"

        return chat_lang

    def cell_lookup(self, chat_id):
        cell_lookup_row = "None"
        try:
            cell_lookup = self.wks_dt.find(str(chat_id))
            cell_lookup_row = 'Data!A' + \
                str(cell_lookup.row) + ":J" + str(cell_lookup.row)
        except Exception as e:
            print(str(e))
            cell_lookup_row = "None"
        print("Cell_lookup Success " + cell_lookup_row)
        return cell_lookup_row
