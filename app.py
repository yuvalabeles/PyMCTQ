# app.py

import streamlit as st

from google_sheets import append_row_to_sheet
from mctq_logic import (
    DAY_TYPES,
    TIME_QUESTIONS,
    VALID_GENDERS,
    WORK_DAY_OPTIONS,
    VALID_YES_NO,
    validate_mctq_answers,
    get_suspicious_time_warnings,
    answers_dict_to_row,
)


st.set_page_config(
    page_title="MCTQ Questionnaire",
    page_icon="🕒",
    layout="centered",
)


if "show_time_confirmations" not in st.session_state:
    st.session_state.show_time_confirmations = False

if "time_warning_data" not in st.session_state:
    st.session_state.time_warning_data = {}

if "show_bottom_time_warning" not in st.session_state:
    st.session_state.show_bottom_time_warning = False


st.title("MCTQ Questionnaire")

st.write(
    "This is an interactive version of the MCTQ questionnaire. "
    "Please enter each answer according to the specified format. "
    "If you need to revise an answer, you can do so before submitting."
)

st.info("For time questions, please use a 24-hour HH:MM format, for example: 23:30.")


with st.form("mctq_form"):
    answers_dict = {}

    st.subheader("General Information")

    answers_dict["full_name"] = st.text_input("Full name")

    answers_dict["gender"] = st.selectbox(
        "Gender",
        options=[""] + VALID_GENDERS,
    )

    answers_dict["WD"] = st.selectbox(
        "How many work days per week do you have?",
        options=[""] + WORK_DAY_OPTIONS,
    )

    st.subheader("Sleep Schedule")

    time_confirmations = {}

    for day_label, suffix in DAY_TYPES:
        st.markdown(f"### {day_label}")

        for question in TIME_QUESTIONS:
            key = question["abbr"] + suffix

            if question["type"] == "time":
                answers_dict[key] = st.text_input(
                    question["label"],
                    placeholder="--:--",
                    key=key,
                )

            else:
                answers_dict[key] = st.text_input(
                    question["label"],
                    placeholder="minutes",
                    key=key,
                )

        relevant_keys = [
            key for key in st.session_state.time_warning_data
            if key.endswith(suffix)
        ]

        for warning_key in relevant_keys:
            warning_data = st.session_state.time_warning_data[warning_key]

            time_confirmations[warning_key] = st.checkbox(
                f"Please note: you entered {warning_data['value']} for your "
                f"{warning_data['description']}, which means {warning_data['value']} in the morning. "
                f"If you meant night-time, please change it to {warning_data['corrected_time']}. "
                f"If you meant morning, please check this box and submit again.",
                key=f"confirm_{warning_key}",
            )

    st.subheader("Alarm Clock")

    answers_dict["Alarmf"] = st.selectbox(
        "I use an alarm clock on free days",
        options=[""] + VALID_YES_NO,
    )

    st.subheader("Time Spent Outdoors")

    st.write("On average, I spend the following amount of time outdoors in daylight:")

    answers_dict["LEw"] = st.text_input(
        "On workdays: --:-- hours",
        placeholder="--:--",
        key="LEw",
    )

    answers_dict["LEf"] = st.text_input(
        "On free days: --:-- hours",
        placeholder="--:--",
        key="LEf",
    )

    submitted = st.form_submit_button("Submit")


if st.session_state.show_bottom_time_warning:
    st.error(
        "The form was not submitted. Please scroll back to the relevant sleep schedule section and review the warning."
    )


if submitted:
    errors = validate_mctq_answers(answers_dict)
    suspicious_time_warnings = get_suspicious_time_warnings(answers_dict)

    missing_confirmations = []

    for warning_key in suspicious_time_warnings:
        if not time_confirmations.get(warning_key, False):
            missing_confirmations.append(warning_key)

    if errors:
        st.session_state.show_time_confirmations = False
        st.session_state.time_warning_data = {}
        st.session_state.show_bottom_time_warning = False

        st.error("Please fix the following issues before submitting:")

        for error in errors:
            st.write(f"- {error}")

    elif suspicious_time_warnings and missing_confirmations:
        st.session_state.show_time_confirmations = True
        st.session_state.time_warning_data = suspicious_time_warnings
        st.session_state.show_bottom_time_warning = True

        st.rerun()

    else:
        st.session_state.show_time_confirmations = False
        st.session_state.time_warning_data = {}
        st.session_state.show_bottom_time_warning = False

        row = answers_dict_to_row(answers_dict)

        append_row_to_sheet("responses", row)

        st.success("Thank you! Your response was submitted successfully.")
