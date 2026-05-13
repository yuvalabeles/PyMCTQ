# app.py

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from google_sheets import append_row_to_sheet
from mctq_logic import (
    BIRTH_DAYS,
    BIRTH_MONTHS,
    BIRTH_YEARS,
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
    page_title="Munich Chronotype Questionnaire (MCTQ)",
    page_icon="🕒",
    layout="centered",
)


if "show_time_confirmations" not in st.session_state:
    st.session_state.show_time_confirmations = False

if "time_warning_data" not in st.session_state:
    st.session_state.time_warning_data = {}

if "show_bottom_time_warning" not in st.session_state:
    st.session_state.show_bottom_time_warning = False


browser_timezone = streamlit_js_eval(
    js_expressions="Intl.DateTimeFormat().resolvedOptions().timeZone",
    key="browser_timezone",
)


def get_question_image_path(question_abbr):
    # Build image path according to the question abbreviation
    return f"images/{question_abbr}.png"


def show_question_note():
    # Show note between bedtime and sleep preparation questions
    note_text_col, note_image_col = st.columns([5, 1])

    with note_text_col:
        st.markdown(
            "**Note that some people stay awake for some time when in bed!**"
        )

    with note_image_col:
        st.image(
            "images/Note.png",
            width=65,
        )


def show_time_question(time_question, key_):
    # Show one time/sleep question with its matching image
    question_col, image_col = st.columns([5, 1])

    with question_col:
        if time_question["type"] == "time":
            answer = st.text_input(
                time_question["label"],
                placeholder="--:--",
                key=key_,
            )

        else:
            answer = st.text_input(
                time_question["label"],
                placeholder="minutes",
                key=key_,
            )

    with image_col:
        st.image(
            get_question_image_path(time_question["abbr"]),
            width=65,
        )

    return answer


def show_light_exposure_input(label, key_prefix):
    # Show light exposure input using separate hour and minute dropdowns
    st.write(label)

    hour_col, hour_text_col, minute_col, minute_text_col = st.columns([2, 1, 2, 1])

    with hour_col:
        hours = st.selectbox(
            "Hours",
            options=[""] + [str(hour) for hour in range(0, 17)],
            key=f"{key_prefix}_hours",
            label_visibility="collapsed",
        )

    with hour_text_col:
        st.markdown("hours")

    with minute_col:
        minutes = st.selectbox(
            "Minutes",
            options=[""] + [str(minute) for minute in range(0, 60)],
            key=f"{key_prefix}_minutes",
            label_visibility="collapsed",
        )

    with minute_text_col:
        st.markdown("minutes")

    if hours == "" or minutes == "":
        return ""

    return f"{int(hours):02d}:{int(minutes):02d}"


st.title("Munich Chronotype Questionnaire (MCTQ)")

st.write(
    "In this questionnaire, you report on your typical sleep behavior over the past 4 weeks. "
    "We ask about work days and work-free days separately. "
    "Please respond to the questions according to your perception of a standard week that includes "
    "your usual work days and work-free days."
)

st.info("For time questions, please use a 24-hour HH:MM format, for example: 23:30.")


with st.form("mctq_form"):
    answers_dict = {"browser_timezone": browser_timezone or ""}

    st.subheader("Personal Information")

    first_name_col, last_name_col = st.columns(2)

    with first_name_col:
        answers_dict["first_name"] = st.text_input(
            "First name"
        )

    with last_name_col:
        answers_dict["last_name"] = st.text_input(
            "Last name"
        )

    answers_dict["email"] = st.text_input(
        "Email"
    )

    st.write("Date of birth")

    birth_day_col, birth_month_col, birth_year_col = st.columns(3)

    with birth_day_col:
        answers_dict["birth_day"] = st.selectbox(
            "Day",
            options=[""] + BIRTH_DAYS,
        )

    with birth_month_col:
        answers_dict["birth_month"] = st.selectbox(
            "Month",
            options=[""] + BIRTH_MONTHS,
        )

    with birth_year_col:
        answers_dict["birth_year"] = st.selectbox(
            "Year",
            options=[""] + BIRTH_YEARS,
        )

    answers_dict["gender"] = st.selectbox(
        "Gender",
        options=[""] + VALID_GENDERS,
    )

    answers_dict["WD"] = st.selectbox(
        "How many work days per week do you have?",
        options=[""] + WORK_DAY_OPTIONS,
    )

    st.subheader("MCTQ")

    time_confirmations = {}

    for day_label, suffix in DAY_TYPES:
        st.markdown(f"### {day_label}")

        for question in TIME_QUESTIONS:
            key = question["abbr"] + suffix

            answers_dict[key] = show_time_question(question, key)

            if question["abbr"] == "BT":
                show_question_note()

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

    st.write(
        "On average, I spend the following amount of time outdoors in daylight:"
    )

    answers_dict["LEw"] = show_light_exposure_input(
        "On workdays:",
        "LEw",
    )

    answers_dict["LEf"] = show_light_exposure_input(
        "On free days:",
        "LEf",
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
