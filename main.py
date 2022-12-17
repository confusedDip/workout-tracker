import datetime
import requests
from config import *

# Set up the track API POST call
exercise_post_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "content-type": "application/json"
}

query = input("What exercises did you today?\n")
exercise_post_config = {
    "query": query
}

response = requests.post(url=exercise_post_endpoint, json=exercise_post_config, headers=headers)
response.raise_for_status()

# Set up the Sheet API POST call
sheety_post_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}",
}

exercises = response.json()["exercises"]

# Get the current date and time
timestamp = datetime.datetime.now()
date = timestamp.strftime("%d/%m/%Y")
time = timestamp.strftime("%H:%M:%S")

# Iterate through all exercises and update it in the worksheet
for exercise in exercises:
    exercise_name = exercise["name"].title()
    exercise_duration = exercise["duration_min"]
    calories_burned = exercise["nf_calories"]

    sheety_post_config = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name,
            "duration": exercise_duration,
            "calories": calories_burned
        }
    }

    sheety_response = requests.post(url=sheety_post_endpoint, json=sheety_post_config, headers=sheety_headers)
    sheety_response.raise_for_status()

print(f"\nSuccessfully logged {len(exercises)} workout(s) in the sheet:"
      f"https://docs.google.com/spreadsheets/d/15-f1JicqkGT5-CSv8iKfmUHrIr-VWynJTHEQStAUQEc/edit?usp=sharing")

