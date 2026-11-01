import requests
import pandas as pd

BASE_URL = "https://api.openf1.org/v1"


def fetch_openf1_data(endpoint, params):
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)


def load_f1_session(year, country, session_name):
    return fetch_openf1_data(
        "sessions",
        {
            "year": year,
            "country_name": country,
            "session_name": session_name
        }
    )


def load_driver_laps(session_key):
    return fetch_openf1_data(
        "laps",
        {"session_key": int(session_key)}
    )


def load_driver_info(session_key):
    return fetch_openf1_data(
        "drivers",
        {"session_key": int(session_key)}
    )


def load_car_telemetry(session_key, driver_number):
    return fetch_openf1_data(
        "car_data",
        {
            "session_key": int(session_key),
            "driver_number": int(driver_number)
        }
    )