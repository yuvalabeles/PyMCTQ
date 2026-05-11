import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

SHEET_NAME = "MCTQ Responses"


def get_sheet(sheet_name="responses"):
    spreadsheet = client.open(SHEET_NAME)
    return spreadsheet.worksheet(sheet_name)


def append_response(data):
    sheet = get_sheet("responses")
    sheet.append_row(data)
