# mctq_logic.py

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VALID_GENDERS = ["Male", "Female"]
VALID_YES_NO = ["Yes", "No"]

WORK_DAY_OPTIONS = [
    "I do not have a regular work schedule",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
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

WORK_FLEXIBILITY_OPTIONS = [
    "Very flexible",
    "A little flexible",
    "Rather inflexible",
    "Very inflexible",
]

COMMUTE_HOUR_OPTIONS = [
    str(hour) for hour in range(0, 3)
]

COMMUTE_MINUTE_OPTIONS = [
    str(minute) for minute in range(0, 60)
]

STIMULANT_PERIOD_OPTIONS = [
    "Day",
    "Week",
    "Month",
]


STIMULANT_ITEMS = [
    {
        "key": "Cigarettes",
        "display_name": "Cigarettes",
        "prefix": "I smoke",
        "unit": "**cigarettes**",
        "none_option": "I don't smoke",
        "amount_options": (
            ["I don't smoke"]
            + [str(amount) for amount in range(1, 21)]
            + ["More than 20"]
        ),
    },
    {
        "key": "Beer",
        "display_name": "Beer",
        "prefix": "I drink",
        "unit": "bottles of **beer**",
        "none_option": "I don't drink beer",
        "amount_options": (
            ["I don't drink beer"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "Wine",
        "display_name": "Wine",
        "prefix": "I drink",
        "unit": "glasses of **wine**",
        "none_option": "I don't drink wine",
        "amount_options": (
            ["I don't drink wine"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "Liquor",
        "display_name": "Liquor",
        "prefix": "I drink",
        "unit": "glasses of **liquor** (not beer/wine)",
        "none_option": "I don't drink liquor",
        "amount_options": (
            ["I don't drink liquor"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "Coffee",
        "display_name": "Coffee",
        "prefix": "I drink",
        "unit": "cups of **coffee**",
        "none_option": "I don't drink coffee",
        "amount_options": (
            ["I don't drink coffee"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "BlackTea",
        "display_name": "Black tea",
        "prefix": "I drink",
        "unit": "cups of **black tea**",
        "none_option": "I don't drink black tea",
        "amount_options": (
            ["I don't drink black tea"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "CaffeinatedDrinks",
        "display_name": "Caffeinated drinks",
        "prefix": "I drink",
        "unit": "cans of **caffeinated drinks**",
        "none_option": "I don't drink caffeinated drinks",
        "amount_options": (
            ["I don't drink caffeinated drinks"]
            + [str(amount) for amount in range(1, 11)]
            + ["More than 10"]
        ),
    },
    {
        "key": "SleepMedication",
        "display_name": "Sleep medication",
        "prefix": "I take **sleep medication**",
        "unit": "times",
        "none_option": "I don't take sleep medication",
        "amount_options": (
            ["I don't take sleep medication"]
            + [str(amount) for amount in range(1, 11)]
        ),
    },
]

MCTQ_COLUMNS = [
    # Personal Information
    "full_name",
    "email",
    "phone_number",
    "date_of_birth",
    "gender",

    # MCTQ:
    "WD",

    # Workdays
    "BTw",
    "SPrepw",
    "SLatw",
    "SEw",
    "SIw",
    "Alarmw",
    "WakeBeforeAlarmw",

    # Free Days
    "BTf",
    "SPrepf",
    "SLatf",
    "SEf",
    "SIf",
    "Alarmf",
    "CannotChooseSleepTimesf",
    "ReasonChildrenPetsf",
    "ReasonHobbiesf",
    "ReasonOtherf",

    # Time Spent Outdoors
    "LEw",
    "LEf",

    # Work Details
    "ShiftWork3M",
    "WorkStart",
    "WorkEnd",
    "WorkFlexibility",
    "CommuteEnclosed",
    "CommuteNotEnclosed",
    "WorkFromHome",
    "CommuteToTotalMinutes",
    "CommuteFromTotalMinutes",

    # Stimulants
    "CigarettesAmount",
    "CigarettesPeriod",
    "BeerAmount",
    "BeerPeriod",
    "WineAmount",
    "WinePeriod",
    "LiquorAmount",
    "LiquorPeriod",
    "CoffeeAmount",
    "CoffeePeriod",
    "BlackTeaAmount",
    "BlackTeaPeriod",
    "CaffeinatedDrinksAmount",
    "CaffeinatedDrinksPeriod",
    "SleepMedicationAmount",
    "SleepMedicationPeriod",

    # Submission Metadata
    "browser_timezone",
    "submitted_at_utc",
    "submitted_at_local",
]

COLUMN_HEADERS = {
    "full_name": "Full Name",
    "email": "Email",
    "phone_number": "Phone Number",
    "date_of_birth": "Date of Birth",
    "gender": "Gender",

    "WD": "# Workdays",

    "BTw": "Bedtime [w]",
    "SPrepw": "Sleep Prep Time [w]",
    "SLatw": "Sleep Latency [w]",
    "SEw": "Sleep End [w]",
    "SIw": "Sleep Inertia [w]",
    "Alarmw": "Alarm Clock [w]",
    "WakeBeforeAlarmw": "Wake Before Alarm [w]",

    "BTf": "Bedtime [f]",
    "SPrepf": "Sleep Prep Time [f]",
    "SLatf": "Sleep Latency [f]",
    "SEf": "Sleep End [f]",
    "SIf": "Sleep Inertia [f]",
    "Alarmf": "Alarm Clock [f]",
    "CannotChooseSleepTimesf": "Cannot Freely Choose Sleep Times [f]",
    "ReasonChildrenPetsf": "Reason - Children/Pets [f]",
    "ReasonHobbiesf": "Reason - Hobbies [f]",
    "ReasonOtherf": "Reason - Other [f]",

    "LEw": "Light Exposure [w]",
    "LEf": "Light Exposure [f]",

    "ShiftWork3M": "Shift Worker - Last 3 Months",
    "WorkStart": "Usual Work Start",
    "WorkEnd": "Usual Work End",
    "WorkFlexibility": "Work Schedule Flexibility",
    "CommuteEnclosed": "Commute - Enclosed Vehicle",
    "CommuteNotEnclosed": "Commute - Not Enclosed Vehicle",
    "WorkFromHome": "Works at Home",
    "CommuteToTotalMinutes": "Commute to Work [minutes]",
    "CommuteFromTotalMinutes": "Commute from Work [minutes]",

    "CigarettesAmount": "Cigarettes - Amount",
    "CigarettesPeriod": "Cigarettes - Period",
    "BeerAmount": "Beer - Amount",
    "BeerPeriod": "Beer - Period",
    "WineAmount": "Wine - Amount",
    "WinePeriod": "Wine - Period",
    "LiquorAmount": "Liquor - Amount",
    "LiquorPeriod": "Liquor - Period",
    "CoffeeAmount": "Coffee - Amount",
    "CoffeePeriod": "Coffee - Period",
    "BlackTeaAmount": "Black Tea - Amount",
    "BlackTeaPeriod": "Black Tea - Period",
    "CaffeinatedDrinksAmount": "Caffeinated Drinks - Amount",
    "CaffeinatedDrinksPeriod": "Caffeinated Drinks - Period",

    "SleepMedicationAmount": "Sleep Medication - Amount",
    "SleepMedicationPeriod": "Sleep Medication - Period",
    "browser_timezone": "Timezone",
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


def are_valid_commute_duration_parts(hours, minutes):
    # Validate the hour and minute values selected for a commute duration
    hours = clean_text(hours)
    minutes = clean_text(minutes)

    return (
        hours in COMMUTE_HOUR_OPTIONS
        and minutes in COMMUTE_MINUTE_OPTIONS
    )


def commute_duration_to_total_minutes(hours, minutes):
    # Convert separate commute hour/minute selections to total minutes
    hours = clean_text(hours)
    minutes = clean_text(minutes)

    return int(hours) * 60 + int(minutes)


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

    alarmw = normalize_choice(answers_dict.get("Alarmw", ""))

    if alarmw not in VALID_YES_NO:
        errors.append(
            "I use an alarm clock on workdays: Please select either 'Yes' or 'No'."
        )

    wake_before_alarmw = normalize_choice(
        answers_dict.get("WakeBeforeAlarmw", "")
    )

    if alarmw == "Yes" and wake_before_alarmw not in VALID_YES_NO:
        errors.append(
            "If 'Yes', I regularly wake up BEFORE the alarm rings: "
            "Please select either 'Yes' or 'No'."
        )

    alarmf = normalize_choice(answers_dict.get("Alarmf", ""))
    if alarmf not in VALID_YES_NO:
        errors.append("""I use an alarm clock on free days: This field must be either 'Yes' or 'No'.""")

    cannot_choose_sleep_times = normalize_choice(
        answers_dict.get("CannotChooseSleepTimesf", "")
    )

    if cannot_choose_sleep_times not in VALID_YES_NO:
        errors.append(
            "Particular reasons affecting sleep times on free days: "
            "Please select either 'Yes' or 'No'."
        )

    elif cannot_choose_sleep_times == "Yes":
        selected_reasons = [
            answers_dict.get("ReasonChildrenPetsf", False),
            answers_dict.get("ReasonHobbiesf", False),
            answers_dict.get("ReasonOtherf", False),
        ]

        if not any(selected_reasons):
            errors.append(
                "Reasons affecting sleep times on free days: "
                "Please select at least one reason."
            )

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

    # Work Details validation
    shift_work = normalize_choice(
        answers_dict.get("ShiftWork3M", "")
    )

    if shift_work not in VALID_YES_NO:
        errors.append(
            "Shift work during the last 3 months: "
            "Please select either 'Yes' or 'No'."
        )

    elif shift_work == "No":
        if not is_valid_hhmm(
            answers_dict.get("WorkStart", "")
        ):
            errors.append(
                "Usual work schedule start: "
                "Please enter the time in HH:MM format."
            )

        if not is_valid_hhmm(
            answers_dict.get("WorkEnd", "")
        ):
            errors.append(
                "Usual work schedule end: "
                "Please enter the time in HH:MM format."
            )

    work_flexibility = normalize_choice(
        answers_dict.get("WorkFlexibility", "")
    )

    if work_flexibility not in WORK_FLEXIBILITY_OPTIONS:
        errors.append(
            "Work schedule flexibility: "
            "Please select one option."
        )

    commute_enclosed = bool(
        answers_dict.get("CommuteEnclosed", False)
    )
    commute_not_enclosed = bool(
        answers_dict.get("CommuteNotEnclosed", False)
    )
    work_from_home = bool(
        answers_dict.get("WorkFromHome", False)
    )

    if not any([
        commute_enclosed,
        commute_not_enclosed,
        work_from_home,
    ]):
        errors.append(
            "Travel to work: Please select at least one option."
        )

    has_physical_commute = (
        commute_enclosed or commute_not_enclosed
    )

    if has_physical_commute:
        if not are_valid_commute_duration_parts(
            answers_dict.get("CommuteToHours", ""),
            answers_dict.get("CommuteToMinutePart", ""),
        ):
            errors.append(
                "Commute to work: "
                "Please select both hours and minutes."
            )

        if not are_valid_commute_duration_parts(
            answers_dict.get("CommuteFromHours", ""),
            answers_dict.get("CommuteFromMinutePart", ""),
        ):
            errors.append(
                "Commute from work: "
                "Please select both hours and minutes."
            )

    # Stimulants validation
    for item in STIMULANT_ITEMS:
        amount_key = f"{item['key']}Amount"
        period_key = f"{item['key']}Period"

        amount = normalize_choice(
            answers_dict.get(amount_key, "")
        )

        if amount not in item["amount_options"]:
            errors.append(
                f"{item['display_name']}: "
                "Please select an amount."
            )
            continue

        if amount != item["none_option"]:
            period = normalize_choice(
                answers_dict.get(period_key, "")
            )

            if period not in STIMULANT_PERIOD_OPTIONS:
                errors.append(
                    f"{item['display_name']}: "
                    "Please select Day, Week, or Month."
                )

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
    cleaned["phone_number"] = clean_text(
        answers_dict.get("phone_number", "")
    )
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

    cleaned["Alarmw"] = normalize_choice(
        answers_dict.get("Alarmw", "")
    )

    if cleaned["Alarmw"] == "Yes":
        cleaned["WakeBeforeAlarmw"] = normalize_choice(
            answers_dict.get("WakeBeforeAlarmw", "")
        )
    else:
        cleaned["WakeBeforeAlarmw"] = ""

    cleaned["Alarmf"] = normalize_choice(answers_dict.get("Alarmf", ""))

    cleaned["CannotChooseSleepTimesf"] = normalize_choice(
        answers_dict.get("CannotChooseSleepTimesf", "")
    )

    if cleaned["CannotChooseSleepTimesf"] == "Yes":
        cleaned["ReasonChildrenPetsf"] = (
            "Yes" if answers_dict.get("ReasonChildrenPetsf", False) else "No"
        )
        cleaned["ReasonHobbiesf"] = (
            "Yes" if answers_dict.get("ReasonHobbiesf", False) else "No"
        )
        cleaned["ReasonOtherf"] = (
            "Yes" if answers_dict.get("ReasonOtherf", False) else "No"
        )
    else:
        cleaned["ReasonChildrenPetsf"] = ""
        cleaned["ReasonHobbiesf"] = ""
        cleaned["ReasonOtherf"] = ""

    cleaned["LEw"] = format_time_answer(answers_dict.get("LEw", ""))
    cleaned["LEf"] = format_time_answer(answers_dict.get("LEf", ""))

    # Work Details
    cleaned["ShiftWork3M"] = normalize_choice(
        answers_dict.get("ShiftWork3M", "")
    )

    if cleaned["ShiftWork3M"] == "No":
        cleaned["WorkStart"] = format_time_answer(
            answers_dict.get("WorkStart", "")
        )
        cleaned["WorkEnd"] = format_time_answer(
            answers_dict.get("WorkEnd", "")
        )
    else:
        cleaned["WorkStart"] = ""
        cleaned["WorkEnd"] = ""

    cleaned["WorkFlexibility"] = normalize_choice(
        answers_dict.get("WorkFlexibility", "")
    )

    cleaned["CommuteEnclosed"] = (
        "Yes"
        if answers_dict.get("CommuteEnclosed", False)
        else "No"
    )

    cleaned["CommuteNotEnclosed"] = (
        "Yes"
        if answers_dict.get("CommuteNotEnclosed", False)
        else "No"
    )

    cleaned["WorkFromHome"] = (
        "Yes"
        if answers_dict.get("WorkFromHome", False)
        else "No"
    )

    has_physical_commute = (
        answers_dict.get("CommuteEnclosed", False)
        or answers_dict.get("CommuteNotEnclosed", False)
    )

    if has_physical_commute:
        cleaned["CommuteToTotalMinutes"] = (
            commute_duration_to_total_minutes(
                answers_dict.get("CommuteToHours", ""),
                answers_dict.get("CommuteToMinutePart", ""),
            )
        )

        cleaned["CommuteFromTotalMinutes"] = (
            commute_duration_to_total_minutes(
                answers_dict.get("CommuteFromHours", ""),
                answers_dict.get("CommuteFromMinutePart", ""),
            )
        )

    else:
        cleaned["CommuteToTotalMinutes"] = ""
        cleaned["CommuteFromTotalMinutes"] = ""

    # Stimulants
    for item in STIMULANT_ITEMS:
        amount_key = f"{item['key']}Amount"
        period_key = f"{item['key']}Period"

        amount = normalize_choice(
            answers_dict.get(amount_key, "")
        )

        cleaned[amount_key] = amount

        if amount == item["none_option"]:
            cleaned[period_key] = ""
        else:
            cleaned[period_key] = normalize_choice(
                answers_dict.get(period_key, "")
            )

    return cleaned


def answers_dict_to_row(answers_dict):
    # Convert answers dictionary into a row ordered by MCTQ_COLUMNS
    cleaned = prepare_answers_for_saving(answers_dict)

    return [cleaned.get(col, "") for col in MCTQ_COLUMNS]
