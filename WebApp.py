import streamlit as st
from databaseHWD import *
import os
import sys
from firebase_admin import db
import pandas as pd
from datetime import datetime

def restart_streamlit():
    os.execv(sys.executable, ['python'] + sys.argv)

# Function to create or get session state
def get_session_state():
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

# Function to get the current LED state from Firebase
def get_led_state_from_firebase():
    ref = db.reference("/")
    return ref.get().get("LED_VAL", 0)

# Function to send data to Firebase Realtime Database
def send_data_to_firebase(data):
    db.reference().update(data)

# Function to create or get session state
def get_session_state():
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = get_led_state_from_firebase() == 1


# Get or create session state
get_session_state()

# Get the current LED state
current_led_state = get_led_state_from_firebase()

st.title("Time Database of Handwashing Detection System-001")

# Create a button to switch the LED state
btn_lbl = 'Switch LED ON/OFF'
button_clicked = st.button(btn_lbl)

key = "LED_VAL"
# Update session state only if the button is clicked
if button_clicked:
    st.session_state.button_clicked = not st.session_state.button_clicked

# Display a message based on the button state
if st.session_state.button_clicked:
    send_data_to_firebase({key: 1})
    st.markdown('<p style="color: green;">The LED is currently ON</p>', unsafe_allow_html=True)
else:
    # Only update the value if the button is clicked, else fetch the current state
    if button_clicked:
        send_data_to_firebase({key: 0})

    st.markdown('<p style="color: red;">The LED is currently OFF</p>', unsafe_allow_html=True)


# Display the current LED state fetched from Firebase
#st.markdown(f'<p>Current LED state from RPI: {current_led_state}</p>', unsafe_allow_html=True)


#st.title("Database of Handwashing Detection System")
df = database.reset_index(drop='index')

# Display the DataFrame
# st.dataframe(df)

# Add a text input for column selection
column_to_search = st.selectbox("Select a column to search:", database.columns[1:])

# Fetch the latest data from Firebase when the search button is clicked
if st.button("Search"):
    # Get the selected date from the user
    selected_date = st.date_input("Select a date:", datetime.now().date())

    # Fetch the latest data for the selected date from Firebase
    # Assuming your Firebase structure includes a "Date" field
    latest_data = db.reference("your_data_path").order_by_child("Date").equal_to(str(selected_date)).get()

    if latest_data:
        # Convert the latest data to a DataFrame and display it
        latest_df = pd.DataFrame(list(latest_data.values()))
        st.subheader(f"Search Results for {selected_date}:")
        st.dataframe(latest_df)
    else:
        st.warning(f"No data found for {selected_date}")
