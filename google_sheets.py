# google_sheets.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def connect_to_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    return client


def open_sheet(sheet_name):
    client = connect_to_google_sheets()

    spreadsheet = client.open("MCTQ Responses")

    worksheet = spreadsheet.worksheet(sheet_name)

    return worksheet


def append_row_to_sheet(sheet_name, row_data):
    worksheet = open_sheet(sheet_name)

    worksheet.append_row(row_data)
