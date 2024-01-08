import streamlit as st
from databaseHWD import *
import os
import sys
from firebase_admin import db
import pandas as pd
from datetime import datetime

def restart_streamlit():
    os.execv(sys.executable, ['python'] + sys.argv)

# Function to get or create session state
def get_session_state():
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = get_led_state_from_firebase() == 1

# Function to get the current LED state from Firebase
def get_led_state_from_firebase():
    ref = db.reference("/")
    return ref.get().get("LED_VAL", 0)

# Function to send data to Firebase Realtime Database
def send_data_to_firebase(data):
    db.reference().update(data)

# Function to get the list of unique dates from the JSON keys and sort them as datetime objects
def get_dates_list():
    dates_list = []
    for date in database.keys():
        if date != "Time":  # Skip the key named "Time"
            try:
                dates_list.append(datetime.strptime(date, "%d-%a:%B:%Y"))
            except ValueError:
                st.error(f"Error parsing date: {date}. Skipping.")
    return sorted(dates_list, reverse=True)

# Get or create session state
get_session_state()

# Get the list of unique dates
dates_list = get_dates_list()

# Convert the sorted dates back to strings for the dropdown
dates_list_str = [date.strftime("%d-%a:%B:%Y") for date in dates_list]

# Create the dropdown with sorted dates
selected_date = st.selectbox("Select a date:", dates_list_str)

# Add a button to trigger the search
search_button = st.button("Search")

# Perform search when the button is clicked
if search_button:
    # Fetch the latest data for the selected date from Firebase
    latest_data = db.reference().child(selected_date).get()

    if latest_data:
        # Convert the latest data to a DataFrame and display it
        latest_df = pd.DataFrame(list(latest_data.items()), columns=["Time", "Value"])
        st.subheader(f"Time Durations of Hand Wash Activity recorded for {selected_date}:")
        st.dataframe(latest_df.style.set_table_styles([{'selector': 'table', 'props': [('max-width', '500px')]}]))
    else:
        st.warning(f"No data found for {selected_date}")
