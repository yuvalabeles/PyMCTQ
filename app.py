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
    COMMUTE_HOUR_OPTIONS,
    COMMUTE_MINUTE_OPTIONS,
    WORK_FLEXIBILITY_OPTIONS,
    STIMULANT_ITEMS,
    STIMULANT_PERIOD_OPTIONS,
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

if "submitted_successfully" not in st.session_state:
    st.session_state.submitted_successfully = False


browser_timezone = streamlit_js_eval(
    js_expressions="Intl.DateTimeFormat().resolvedOptions().timeZone",
    key="browser_timezone",
)


def get_question_image_path(question_abbr):
    # Build image path according to the question abbreviation
    return f"images/{question_abbr}.png"


def show_question_note():
    # Show note between bedtime and sleep preparation questions
    image_col, note_text_col, empty_col = st.columns([1.5, 7, 0.5])

    with image_col:
        st.image(
            "images/Note.png",
            width=80,
        )

    with note_text_col:
        st.markdown(
            "**Note that some people stay awake for some time when in bed!**"
        )

    with empty_col:
        st.write("")

    divide(p=0.5)


def show_time_question(time_question, key_, t="23:00"):
    # Show image, question, and answer field in one row
    image_col, question_col, input_col = st.columns([1.5, 5, 2.8])

    with image_col:
        st.image(
            get_question_image_path(time_question["abbr"]),
            width=80,
        )

    with question_col:
        st.markdown(
            f"<div style='padding-top: 8px'>{time_question['label']}</div>",
            unsafe_allow_html=True,
        )

    with input_col:
        if time_question["type"] == "time":
            answer = st.text_input(
                "Time input",
                placeholder=f"HH:MM (e.g. {t})",
                key=key_,
                label_visibility="collapsed",
            )

        else:
            answer = st.text_input(
                "Minutes input",
                placeholder="minutes only (e.g. 10)",
                key=key_,
                label_visibility="collapsed",
            )

    divide(p=0.5)

    return answer


def show_yes_no_question(label, k, caption=None):
    question_col, answer_col = st.columns(
        [6, 2],
        vertical_alignment="center",
    )

    with question_col:
        st.markdown(f"**{label}**")

    if caption is not None:
        st.caption(caption)

    with answer_col:
        answer = st.radio(
            label,
            options=VALID_YES_NO,
            index=None,
            horizontal=True,
            key=k,
            label_visibility="collapsed",
        )

    divide(p=0.5)

    return answer


def show_light_exposure_input(label, key_prefix):
    # Show light exposure input using separate hour and minute dropdowns
    (
        label_col, hour_col, minute_col, minute_text_col
    ) = st.columns([1.5, 1.4, 1.4, 3.5],
                   vertical_alignment="center")

    with label_col:
        st.write(label)

    with hour_col:
        hours = st.selectbox(
            "Hours",
            options=[""] + [str(hour) for hour in range(0, 17)],
            key=f"{key_prefix}_hours",
        )

    with minute_col:
        minutes = st.selectbox(
            "Minutes",
            options=[""] + [str(minute) for minute in range(0, 60)],
            key=f"{key_prefix}_minutes",
        )

    if hours == "" or minutes == "":
        return ""

    return f"{int(hours):02d}:{int(minutes):02d}"


def show_commute_duration_input(label, key_prefix):
    # Show separate dropdowns for commute hours and minutes
    (
        label_col,
        hour_col,
        minute_col,
        minute_text_col,
    ) = st.columns(
        [4.5, 1.2, 1.4, 1.5],
        vertical_alignment="center",
    )

    with label_col:
        st.markdown(label, unsafe_allow_html=True)

    with hour_col:
        hours = st.selectbox(
            f"Hours",
            options=[""] + COMMUTE_HOUR_OPTIONS,
            key=f"{key_prefix}_hours",
        )

    with minute_col:
        minutes = st.selectbox(
            f"Minutes",
            options=[""] + COMMUTE_MINUTE_OPTIONS,
            key=f"{key_prefix}_minutes",
        )

    return hours, minutes


def show_stimulant_row(itm, medication=False):
    st.markdown(
        """
        <style>
        /* Text next to radio buttons */
        div[data-testid="stRadio"] div[role="radiogroup"] label p {
            font-size: 15px !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    # First row: statement, amount, and unit
    if medication:
        amount_col, unit_col = st.columns(
            [4.5, 5],
            vertical_alignment="center",
        )
    else:
        amount_col, unit_col = st.columns(
            [4, 6],
            vertical_alignment="center",
        )

    with amount_col:
        amount = st.selectbox(
            itm["prefix"],
            options=[""] + itm["amount_options"],
            key=f"{itm['key']}Amount",
            # label_visibility="collapsed",
        )

    with unit_col:
        period = st.radio(
            itm["unit"] + "\u00A0\u00A0per:",
            options=STIMULANT_PERIOD_OPTIONS,
            index=None,
            horizontal=True,
            key=f"{itm['key']}Period",
            # label_visibility="collapsed",
        )

    st.markdown(
        "<div style='height: 8px'></div>",
        unsafe_allow_html=True,
    )

    return amount, period


def divide(p=3.0):
    st.markdown(
        f"""
        <div style="
            border-top: {p}px solid rgba(128, 128, 128, 0.35);
            margin: 14px 0 18px 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )


st.title("Munich Chronotype Questionnaire (MCTQ)")

st.write(
    "In this questionnaire, you report on your typical sleep behavior over the past 4 weeks. "
    "We ask about work days and work-free days separately. "
    "Please respond to the questions according to your perception of a standard week that includes "
    "your usual work days and work-free days."
)

# TODO - replace all info in [] below:
st.markdown(
    """
    #### Participation and use of information

    This questionnaire is part of a research project on chronotype and sleep-wake patterns conducted by 
    [laboratory / principal investigator] at the Weizmann Institute of Science.

    Participation is voluntary. The information you provide, including identifying and contact information, 
    will be securely stored and used only for the research purposes described here. 
    Access to the information will be restricted to authorized members of the research team.

    Results may be presented in scientific publications, presentations, or reports only in aggregate or de-identified form, 
    without your name, contact details, or other information reasonably expected to identify you.

    The information will be retained for [retention period] and may be accessed by [authorized recipients]. 
    You are not legally required to provide this information. 

    For questions or requests concerning your personal information, please contact [name and institutional email]. 
    [Link to the full participant information and privacy notice.]
    """
)

st.info("For time questions, please use a 24-hour HH:MM format, for example: 23:30.")

if st.session_state.submitted_successfully:
    st.success(
        "Thank you! Your response was submitted successfully. "
        "You may now close this page."
    )
    st.stop()

with st.form("mctq_form"):
    answers_dict = {"browser_timezone": browser_timezone or ""}

    st.markdown("### Personal Information")

    first_name_col, last_name_col = st.columns(2)

    with first_name_col:
        answers_dict["first_name"] = st.text_input(
            "**First name:**"
        )

    with last_name_col:
        answers_dict["last_name"] = st.text_input(
            "**Last name:**"
        )

    answers_dict["email"] = st.text_input(
        "**Email:**"
    )

    answers_dict["phone_number"] = st.text_input(
        "**Phone number:** (optional)",
    )

    st.markdown(
        "<span style='font-size: 14px;'>**Date of birth:**</span>",
        unsafe_allow_html=True,
    )

    birth_day_col, birth_month_col, birth_year_col = st.columns(3)

    with birth_day_col:
        answers_dict["birth_day"] = st.selectbox(
            "Day",
            options=[""] + BIRTH_DAYS,
            placeholder="dd",
        )

    with birth_month_col:
        answers_dict["birth_month"] = st.selectbox(
            "Month",
            options=[""] + BIRTH_MONTHS,
            placeholder="mm",
        )

    with birth_year_col:
        answers_dict["birth_year"] = st.selectbox(
            "Year",
            options=[""] + BIRTH_YEARS,
            placeholder="yyyy",
        )

    q_col, radio_col, empt_col = st.columns(
        [1, 4, 4],
        vertical_alignment="center",
    )

    with q_col:
        st.markdown("<span style='font-size: 14px;'>**Gender:**</span>",
                    unsafe_allow_html=True,)

    with radio_col:
        answers_dict["gender"] = st.radio(
            "Gender:",
            options=VALID_GENDERS,
            index=None,
            horizontal=True,
            key="gender",
            label_visibility="collapsed",
        )

    divide()

    st.markdown("## MCTQ")

    answers_dict["WD"] = st.selectbox(
        "**How many work days per week do you have?** (this includes being, for example, a stay-at-home parent)",
        options=[""] + WORK_DAY_OPTIONS,
    )

    st.caption("Note: if your answer is '7' or 'I do not have a regular work schedule', "
               "please consider if your sleep times may still differ between regular 'workdays' "
               "and 'weekend days' and fill this MCTQ accordingly."
               "\n\nIn that case, please also change the answer above to reflect that.")

    time_confirmations = {}

    for day_label, suffix in DAY_TYPES:
        st.markdown(f"#### <u>{day_label}:</u>",
                    unsafe_allow_html=True,
                    )

        for question in TIME_QUESTIONS:
            key = question["abbr"] + suffix

            if question["abbr"] == "SE":
                answers_dict[key] = show_time_question(question, key, t="08:10")
            elif question["abbr"] == "SPrep":
                answers_dict[key] = show_time_question(question, key, t="23:30")
            else:
                answers_dict[key] = show_time_question(question, key)

            if question["abbr"] == "BT":
                show_question_note()

        if suffix == "w":
            answers_dict["Alarmw"] = show_yes_no_question(
                "I use an alarm clock on workdays:",
                "Alarmw",
            )

            answers_dict["WakeBeforeAlarmw"] = show_yes_no_question(
                "If 'Yes' - I regularly wake up BEFORE the alarm rings:",
                "WakeBeforeAlarmw",
            )

        if suffix == "f":
            answers_dict["Alarmf"] = show_yes_no_question(
                "My wake-up time is due to the use of an alarm clock:",
                "Alarmf",
            )

            answers_dict["CannotChooseSleepTimesf"] = show_yes_no_question(
                "There are specific reasons I use an alarm clock on work-free days:",
                "CannotChooseSleepTimesf",
            )

            st.markdown("**If 'Yes' - please select all the reasons that apply:**")

            children_col, hobbies_col, other_col = st.columns(3)

            with children_col:
                answers_dict["ReasonChildrenPetsf"] = st.checkbox(
                    "Child(ren)/pet(s)",
                    key="ReasonChildrenPetsf",
                )

            with hobbies_col:
                answers_dict["ReasonHobbiesf"] = st.checkbox(
                    "Hobbies",
                    key="ReasonHobbiesf",
                )

            with other_col:
                answers_dict["ReasonOtherf"] = st.checkbox(
                    "Other",
                    key="ReasonOtherf",
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

    divide()
    st.markdown("### Time Spent Outdoors")

    st.write(
        "On average, I spend the following amount of time outdoors in daylight:"
    )

    answers_dict["LEw"] = show_light_exposure_input(
        "**Workdays:**",
        "LEw",
    )

    divide(p=0.5)

    answers_dict["LEf"] = show_light_exposure_input(
        "**Free days:**",
        "LEf",
    )

    divide()
    st.markdown("### Work Details")

    answers_dict["ShiftWork3M"] = show_yes_no_question(
        "In the last 3 months, I worked as a shift worker:",
        "ShiftWork3M",
        caption="(if 'Yes' - please skip 'Daily work schedule' section, "
                "and continue with 'Work schedules flexibility' section)"
    )

    st.markdown("**Daily work schedule:** (optional)")

    (
        start_input_col,
        end_input_col,
        space_col
    ) = st.columns(
        [1.5, 1.5, 5],
        vertical_alignment="center",
    )

    with start_input_col:
        answers_dict["WorkStart"] = st.text_input(
            "Starts at:",
            placeholder="HH:MM",
            key="WorkStart",
            # label_visibility="collapsed",
        )

    with end_input_col:
        answers_dict["WorkEnd"] = st.text_input(
            "Ends at:",
            placeholder="HH:MM",
            key="WorkEnd",
            # label_visibility="collapsed",
        )

    divide(p=0.5)

    st.markdown("**Workdays schedule flexibility:**")

    answers_dict["WorkFlexibility"] = st.radio(
        "My work schedules are - ",
        options=WORK_FLEXIBILITY_OPTIONS,
        index=None,
        horizontal=False,
        key="WorkFlexibility",
    )

    divide(p=0.5)

    st.markdown("**I commute to work:**")
    st.caption("(if needed, you can choose more than one)")
    answers_dict["CommuteEnclosed"] = st.checkbox(
        "Within an enclosed vehicle "
        "(e.g. car, bus, underground).",
        key="CommuteEnclosed",
    )

    answers_dict["CommuteNotEnclosed"] = st.checkbox(
        "Not within an enclosed vehicle "
        "(e.g. on foot, by bike).",
        key="CommuteNotEnclosed",
    )

    answers_dict["WorkFromHome"] = st.checkbox(
        "I work at home.",
        key="WorkFromHome",
    )

    divide(p=0.5)

    (
        answers_dict["CommuteToHours"],
        answers_dict["CommuteToMinutePart"],
    ) = show_commute_duration_input(
        "**The commute <u>to</u> work takes me:**",
        "commute_to",
    )

    divide(p=0.5)

    (
        answers_dict["CommuteFromHours"],
        answers_dict["CommuteFromMinutePart"],
    ) = show_commute_duration_input(
        "**The commute <u>from</u> work takes me:**",
        "commute_from",
    )

    divide()
    st.markdown("### Stimulants")

    st.markdown(
        "Please give <u>approximate/average amounts</u>:",
        unsafe_allow_html=True,
    )

    for index, item in enumerate(STIMULANT_ITEMS):
        if item['key'] == "SleepMedication":
            sleep_med = True
        else:
            sleep_med = False
        amount_key = f"{item['key']}Amount"
        period_key = f"{item['key']}Period"

        (
            answers_dict[amount_key],
            answers_dict[period_key],
        ) = show_stimulant_row(item, medication=sleep_med)

        # Add a short divider between items, but not after the last one
        if index < len(STIMULANT_ITEMS) - 1:
            left_space, divider_col, right_space = st.columns([0.2, 8, 0.2])

            with divider_col:
                divide(p=1)

    divide()

    st.markdown("### Consent")

    answers_dict["research_consent"] = st.checkbox(
        "I have read and understood the information above. "
        "I voluntarily agree to participate in this study and consent to "
        "the collection, storage, and use of my questionnaire responses "
        "for research on chronotype and sleep-wake patterns, as described above.",
        value=False,
        key="research_consent",
    )

    answers_dict["future_contact_consent"] = st.checkbox(
        "(Optional) I agree that the research team may use my questionnaire "
        "responses to assess whether I may be eligible for future studies "
        "related to chronotype and sleep, and may contact me using the contact "
        "details I provided. I understand that this does not oblige me to "
        "participate in any future study.",
        value=False,
        key="future_contact_consent",
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

        st.session_state.submitted_successfully = True
        st.rerun()
