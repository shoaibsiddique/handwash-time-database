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






# Convert the date strings to datetime objects
database['Datetime'] = pd.to_datetime(database.index, format='%d-%a:%B:%Y')

# Sort the DataFrame by the datetime column in descending order
database = database.sort_values(by='Datetime', ascending=False)

# Remove the 'Datetime' column as it was only used for sorting
database = database.drop('Datetime', axis=1)

# Fetch unique values from the column and sort them in descending order
unique_values = sorted(database[column_to_search].unique(), reverse=True)

# Add a text input for column selection
column_to_search = st.selectbox("Select a column to search:", unique_values)

# Add a button to trigger the search
search_button = st.button("Search")

# Perform search when the button is clicked
if search_button:
    if column_to_search in df.columns:
        st.subheader(f"Search Results for {column_to_search}:")
        st.dataframe(database[["Time", column_to_search]].dropna().reset_index(drop='index'))
    else:
        st.warning(f"Column '{column_to_search}' not found in the DataFrame.")
