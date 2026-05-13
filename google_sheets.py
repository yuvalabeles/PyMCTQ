# google_sheets.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

from mctq_logic import READABLE_HEADERS


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


def open_spreadsheet():
    client = connect_to_google_sheets()

    spreadsheet = client.open("MCTQ Responses")

    return spreadsheet


def open_sheet(sheet_name):
    spreadsheet = open_spreadsheet()

    worksheet = spreadsheet.worksheet(sheet_name)

    return worksheet


def set_header_column_widths(worksheet):
    spreadsheet = open_spreadsheet()

    requests = []

    for index, header in enumerate(READABLE_HEADERS):
        pixel_size = max(90, min(len(header) * 7 + 15, 250))

        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": index,
                        "endIndex": index + 1,
                    },
                    "properties": {
                        "pixelSize": pixel_size,
                    },
                    "fields": "pixelSize",
                }
            }
        )

    spreadsheet.batch_update({"requests": requests})


def ensure_headers_exist(worksheet):
    existing_values = worksheet.get_all_values()

    # Sheet completely empty
    if len(existing_values) == 0:
        worksheet.append_row(READABLE_HEADERS)
        set_header_column_widths(worksheet)

    else:
        existing_headers = existing_values[0]

        # Replace headers if they are different from the current readable headers
        if existing_headers != READABLE_HEADERS:
            worksheet.batch_clear(["1:1"])
            worksheet.update("A1", [READABLE_HEADERS])
            set_header_column_widths(worksheet)

    # Make the header row bold
    worksheet.format("1:1", {"textFormat": {"bold": True}})


def append_row_to_sheet(sheet_name, row):
    worksheet = open_sheet(sheet_name)

    ensure_headers_exist(worksheet)

    worksheet.append_row(row)
