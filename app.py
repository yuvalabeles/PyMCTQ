import streamlit as st
from datetime import datetime

from google_sheets import append_response

st.title("MCTQ Questionnaire")

name = st.text_input("Enter your name")

if st.button("Submit"):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    append_response([
        timestamp,
        "",
        name
    ])

    st.success("Response submitted!")
