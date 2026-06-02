# mctq_logic.py

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VALID_GENDERS = ["Male", "Female"]
VALID_YES_NO = ["Yes", "No"]

WORK_DAY_OPTIONS = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "I do not have a regular work schedule",
]

BIRTH_DAYS = [str(day) for day in range(1, 32)]
BIRTH_MONTHS = [str(month) for month in range(1, 13)]
BIRTH_YEARS = [str(year) for year in range(date.today().year - 5, date.today().year - 100, -1)]

DAY_TYPES = [
    ("Workdays", "w"),
    ("Free Days", "f"),
]

TIME_QUESTIONS = [
    {
        "abbr": "BT",
        "label": "I go to bed at:",
        "type": "time",
    },
    {
        "abbr": "SPrep",
        "label": "I actually get ready to fall asleep at:",
        "type": "time",
    },
    {
        "abbr": "SLat",
        "label": "I need ☐ minutes to fall asleep:",
        "type": "minutes",
    },
    {
        "abbr": "SE",
        "label": "I wake up at:",
        "type": "time",
    },
    {
        "abbr": "SI",
        "label": "After ☐ minutes, I get up:",
        "type": "minutes",
    },
]

MCTQ_COLUMNS = [
    "full_name",
    "email",
    "date_of_birth",
    "gender",
    "browser_timezone",
    "WD",
    "BTw",
    "SPrepw",
    "SLatw",
    "SEw",
    "SIw",
    "BTf",
    "SPrepf",
    "SLatf",
    "SEf",
    "SIf",
    "Alarmf",
    "LEw",
    "LEf",
    "submitted_at_utc",
    "submitted_at_local",
]

COLUMN_HEADERS = {
    "full_name": "Full Name",
    "email": "Email",
    "date_of_birth": "Date of Birth",
    "gender": "Gender",
    "browser_timezone": "Timezone",
    "WD": "# Workdays",
    "BTw": "Bedtime [w]",
    "SPrepw": "Sleep Prep Time [w]",
    "SLatw": "Sleep Latency [w]",
    "SEw": "Sleep End [w]",
    "SIw": "Sleep Inertia [w]",
    "BTf": "Bedtime [f]",
    "SPrepf": "Sleep Prep Time [f]",
    "SLatf": "Sleep Latency [f]",
    "SEf": "Sleep End [f]",
    "SIf": "Sleep Inertia [f]",
    "Alarmf": "Alarm Clock [f]",
    "LEw": "Light Exposure [w]",
    "LEf": "Light Exposure [f]",
    "submitted_at_utc": "Submission Time - UTC",
    "submitted_at_local": "Submission Time - Local",
}

READABLE_HEADERS = [
    COLUMN_HEADERS[col]
    for col in MCTQ_COLUMNS
]

SUSPICIOUS_TIME_FIELDS = {
    "BTw": "bedtime on workdays",
    "SPrepw": "time you get ready to fall asleep on workdays",
    "BTf": "bedtime on free days",
    "SPrepf": "time you get ready to fall asleep on free days",
}


def clean_text(value):
    # Remove leading and trailing spaces
    if value is None:
        return ""
    return str(value).strip()


def clean_no_spaces(value):
    # Remove all spaces from the answer
    if value is None:
        return ""
    return str(value).replace(" ", "")


def normalize_choice(value):
    # Clean choice answers
    return clean_text(value)


def build_full_name(first_name, last_name):
    # Combine first and last name into one full name
    first_name = clean_text(first_name)
    last_name = clean_text(last_name)

    return " ".join(part for part in [first_name, last_name] if part != "")


def get_submission_metadata(browser_timezone=None):
    # Create UTC and local submission timestamps
    submitted_at_utc_dt = datetime.now(timezone.utc)
    submitted_at_utc = submitted_at_utc_dt.isoformat(timespec="seconds")

    browser_timezone = clean_text(browser_timezone)

    if browser_timezone:
        try:
            submitted_at_local = submitted_at_utc_dt.astimezone(
                ZoneInfo(browser_timezone)
            ).isoformat(timespec="seconds")

        except ValueError:
            submitted_at_local = ""

        except ZoneInfoNotFoundError:
            submitted_at_local = ""
    else:
        submitted_at_local = ""

    return {
        "submitted_at_utc": submitted_at_utc,
        "submitted_at_local": submitted_at_local,
        "browser_timezone": browser_timezone,
    }


def format_time_answer(value):
    # Convert H:MM or HH:MM into HH:MM:00
    value = clean_no_spaces(value)

    if value == "":
        return ""

    parsed_time = datetime.strptime(value, "%H:%M")

    return parsed_time.strftime("%H:%M:%S")


def is_valid_hhmm(value):
    # Check if a value is in valid H:MM or HH:MM format
    value = clean_no_spaces(value)

    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def is_valid_number(value):
    # Check if a value is a valid non-negative integer or decimal number
    value = clean_no_spaces(value)

    if value == "":
        return False

    try:
        return float(value) >= 0
    except ValueError:
        return False


def is_valid_email(value):
    # Minimal email validation
    value = clean_text(value)

    return "@" in value and len(value) >= 3


def build_date_of_birth(day, month, year):
    # Build date of birth in YYYY-MM-DD format
    day = clean_no_spaces(day)
    month = clean_no_spaces(month)
    year = clean_no_spaces(year)

    if day == "" or month == "" or year == "":
        return ""

    try:
        birth_date = date(int(year), int(month), int(day))
        return birth_date.isoformat()
    except ValueError:
        return ""


def calculate_age(birth_date, today=None):
    # Calculate age in full years
    if today is None:
        today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def is_valid_date_of_birth(day, month, year):
    # Validate date of birth and age range
    day = clean_no_spaces(day)
    month = clean_no_spaces(month)
    year = clean_no_spaces(year)

    if day == "" or month == "" or year == "":
        return False

    try:
        birth_date = date(int(year), int(month), int(day))
    except ValueError:
        return False

    age = calculate_age(birth_date)

    return 5 <= age <= 99


def is_range_like(value):
    # Detect common range formats such as 30-40, 30–40, 30 to 40, or 30 40
    value = clean_text(value).lower()

    if " to " in value or "-" in value or "–" in value or "—" in value:
        return True

    parts = value.split()
    if len(parts) == 2 and all(part.replace(".", "", 1).isdigit() for part in parts):
        return True

    return False


def looks_like_hour_minute_duration(value):
    # Detect duration values written like H:MM or HH:MM
    value = clean_no_spaces(value)

    parts = value.split(":")
    if len(parts) != 2:
        return False

    hours, minutes = parts

    return hours.isdigit() and minutes.isdigit() and 0 <= int(minutes) <= 59


def convert_hour_minute_duration_to_minutes(value):
    # Convert H:MM duration format into total minutes
    value = clean_no_spaces(value)
    hours, minutes = value.split(":")

    return int(hours) * 60 + int(minutes)


def convert_minute_second_duration_to_decimal_minutes(value):
    # Convert M:SS duration format into decimal minutes
    value = clean_no_spaces(value)
    minutes, seconds = value.split(":")

    decimal_minutes = int(minutes) + int(seconds) / 60

    if decimal_minutes.is_integer():
        return str(int(decimal_minutes))

    return str(round(decimal_minutes, 2)).rstrip("0").rstrip(".")


def get_minutes_validation_error(value, readable_name):
    # Return a readable error message for invalid minute-duration answers
    value = clean_text(value)

    if value == "":
        return f"""{readable_name}: This field is required."""

    if is_range_like(value):
        return f"""{readable_name}:

    Please enter a single value in minutes, not a range. For example, write 35 instead of 30–40."""

    if looks_like_hour_minute_duration(value):
        converted_minutes = convert_hour_minute_duration_to_minutes(value)
        decimal_minutes = convert_minute_second_duration_to_decimal_minutes(value)

        hours_part, minutes_part = clean_no_spaces(value).split(":")
        hours_part = int(hours_part)
        minutes_part = int(minutes_part)

        hours_label = "hour" if hours_part == 1 else "hours"
        minutes_label = "minute" if minutes_part == 1 else "minutes"
        seconds_label = "second" if minutes_part == 1 else "seconds"

        return f"""{readable_name}: 

    Please enter the duration in minutes only. 
    If you meant {hours_part} {hours_label} and {minutes_part} {minutes_label}, write {converted_minutes}. 
    If you meant {hours_part} minutes and {minutes_part} {seconds_label}, write {decimal_minutes}."""

    if not is_valid_number(value):
        return f"""{readable_name}: Please enter the duration as a single number of minutes. Do not use ranges, hours, or text. For example: 10, 30, 90, or 1.5."""

    return None


def hhmm_to_minutes(value):
    # Convert HH:MM into minutes from midnight
    value = clean_no_spaces(value)
    parsed_time = datetime.strptime(value, "%H:%M")

    return parsed_time.hour * 60 + parsed_time.minute


def get_time_difference_minutes(start_time, end_time):
    # Calculate end_time - start_time, allowing crossing midnight
    start_minutes = hhmm_to_minutes(start_time)
    end_minutes = hhmm_to_minutes(end_time)

    if end_minutes < start_minutes:
        end_minutes += 24 * 60

    return end_minutes - start_minutes


def is_suspicious_time(value):
    # Check if time is between 05:00 and 12:59
    if not is_valid_hhmm(value):
        return False

    minutes = hhmm_to_minutes(value)

    return 5 * 60 <= minutes <= (12 * 60 + 59)


def convert_morning_time_to_night_format(value):
    # Convert suspicious morning time to likely intended night-time format
    value = clean_no_spaces(value)

    hour, minute = value.split(":")
    hour = int(hour)

    if hour == 12:
        corrected_hour = 0
    else:
        corrected_hour = hour + 12

    return f"{corrected_hour:02d}:{minute}"


def get_readable_field_name(key):
    # Convert internal column names into readable names for validation messages
    readable_names = {
        "first_name": "First name",
        "last_name": "Last name",
        "full_name": "Full name",
        "email": "Email",
        "date_of_birth": "Date of birth",
        "birth_day": "Birth day",
        "birth_month": "Birth month",
        "birth_year": "Birth year",
        "gender": "Gender",
        "WD": "Work schedule",
        "Alarmf": "I use an alarm clock on free days",
        "LEw": "Time spent outdoors in daylight on workdays",
        "LEf": "Time spent outdoors in daylight on free days",
    }

    if key in readable_names:
        return readable_names[key]

    for day_label, suffix in DAY_TYPES:
        for question in TIME_QUESTIONS:
            if key == question["abbr"] + suffix:
                return f'{day_label}: "{question["label"]}"'

    return key


def get_suspicious_time_warnings(answers_dict):
    # Return warnings for suspicious bedtime / sleep-preparation values
    warnings = {}

    for key, description in SUSPICIOUS_TIME_FIELDS.items():
        value = clean_no_spaces(answers_dict.get(key, ""))

        if is_suspicious_time(value):
            corrected_time = convert_morning_time_to_night_format(value)

            warnings[key] = {
                "value": value,
                "corrected_time": corrected_time,
                "description": description,
            }

    return warnings


def validate_sleep_preparation_order(answers_dict):
    # Validate that sleep preparation time is after bedtime, allowing midnight crossing
    errors = []

    max_allowed_gap_minutes = 6 * 60

    for day_label, suffix in DAY_TYPES:
        bedtime_key = "BT" + suffix
        sleep_prep_key = "SPrep" + suffix

        bedtime = answers_dict.get(bedtime_key, "")
        sleep_prep = answers_dict.get(sleep_prep_key, "")

        if not is_valid_hhmm(bedtime) or not is_valid_hhmm(sleep_prep):
            continue

        gap_minutes = get_time_difference_minutes(bedtime, sleep_prep)

        if gap_minutes > max_allowed_gap_minutes:
            errors.append(
                f"""{day_label}: Sleep preparation time

    The time you get ready to fall asleep should be after the time you go to bed. The first question refers to the time you get into bed, while the second question refers to the time you close your eyes and start trying to fall asleep. The following question about sleep latency refers to the number of minutes between starting to fall asleep and actually falling asleep."""
            )

    return errors


def validate_mctq_answers(answers_dict):
    # Return a list of readable validation errors
    errors = []

    first_name = clean_text(answers_dict.get("first_name", ""))
    if first_name == "":
        errors.append("""First name: This field is required.""")

    last_name = clean_text(answers_dict.get("last_name", ""))
    if last_name == "":
        errors.append("""Last name: This field is required.""")

    email = clean_text(answers_dict.get("email", ""))
    if not is_valid_email(email):
        errors.append("""Email: Please enter a valid email address.""")

    if not is_valid_date_of_birth(
        answers_dict.get("birth_day", ""),
        answers_dict.get("birth_month", ""),
        answers_dict.get("birth_year", ""),
    ):
        errors.append("""Date of birth: Please enter a valid date of birth for age 5-99.""")

    gender = normalize_choice(answers_dict.get("gender", ""))
    if gender not in VALID_GENDERS:
        errors.append("""Gender: Gender must be either 'Male' or 'Female'.""")

    wd = clean_text(answers_dict.get("WD", ""))
    if wd not in WORK_DAY_OPTIONS:
        errors.append("""Work schedule: Please select your work schedule.""")

    alarmf = normalize_choice(answers_dict.get("Alarmf", ""))
    if alarmf not in VALID_YES_NO:
        errors.append("""I use an alarm clock on free days: This field must be either 'Yes' or 'No'.""")

    for day_label, suffix in DAY_TYPES:
        for question in TIME_QUESTIONS:
            key = question["abbr"] + suffix
            value = answers_dict.get(key, "")
            readable_name = get_readable_field_name(key)

            if question["type"] == "time":
                if not is_valid_hhmm(value):
                    errors.append(f"""{readable_name}: Please enter the time in HH:MM format.""")

            if question["type"] == "minutes":
                minutes_error = get_minutes_validation_error(value, readable_name)

                if minutes_error is not None:
                    errors.append(minutes_error)

    for key in ["LEw", "LEf"]:
        readable_name = get_readable_field_name(key)

        if not is_valid_hhmm(answers_dict.get(key, "")):
            errors.append(f"""{readable_name}: Please enter the time in HH:MM format.""")

    errors.extend(validate_sleep_preparation_order(answers_dict))

    return errors


def prepare_answers_for_saving(answers_dict):
    # Clean and format answers before saving them to Google Sheets
    cleaned = {}

    cleaned.update(get_submission_metadata(answers_dict.get("browser_timezone", "")))

    cleaned["full_name"] = build_full_name(
        answers_dict.get("first_name", ""),
        answers_dict.get("last_name", ""),
    )
    cleaned["email"] = clean_text(answers_dict.get("email", ""))
    cleaned["date_of_birth"] = build_date_of_birth(
        answers_dict.get("birth_day", ""),
        answers_dict.get("birth_month", ""),
        answers_dict.get("birth_year", ""),
    )
    cleaned["gender"] = normalize_choice(answers_dict.get("gender", ""))
    cleaned["WD"] = clean_text(answers_dict.get("WD", ""))

    for day_label, suffix in DAY_TYPES:
        for question in TIME_QUESTIONS:
            key = question["abbr"] + suffix
            value = answers_dict.get(key, "")

            if question["type"] == "time":
                cleaned[key] = format_time_answer(value)
            else:
                cleaned[key] = clean_no_spaces(value)

    cleaned["Alarmf"] = normalize_choice(answers_dict.get("Alarmf", ""))
    cleaned["LEw"] = format_time_answer(answers_dict.get("LEw", ""))
    cleaned["LEf"] = format_time_answer(answers_dict.get("LEf", ""))

    return cleaned


def answers_dict_to_row(answers_dict):
    # Convert answers dictionary into a row ordered by MCTQ_COLUMNS
    cleaned = prepare_answers_for_saving(answers_dict)

    return [cleaned.get(col, "") for col in MCTQ_COLUMNS]
