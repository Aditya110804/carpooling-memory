import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import save_passenger

def show():
    st.header("👤 Passenger Registration")

    with st.form("passenger_form"):
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=18, max_value=100)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        aadhar = st.text_input("Aadhar ID or Unique ID *")
        contact = st.text_input("Contact Number *")
        from_location = st.text_input("Current Location (From) *")
        to_location = st.text_input("Destination (To) *")
        travel_date = st.date_input("Travel Date *")
        travel_time = st.time_input("Travel Time *")

        submitted = st.form_submit_button("Register")

        if submitted:
            required_fields = [name, aadhar, contact, from_location, to_location]
            if any(not str(field).strip() for field in required_fields):
                st.error("Please fill all required fields marked with *.")
            else:
                passenger_data = {
                    "name": name.strip(),
                    "age": int(age),
                    "gender": gender,
                    "aadhar": aadhar.strip(),
                    "contact": contact.strip(),
                    "from": from_location.strip(),
                    "to": to_location.strip(),
                    "date": str(travel_date),
                    "time": travel_time.strftime("%H:%M:%S"),
                }
                save_passenger(passenger_data)
                st.success(f"Thank you {name}! You have been registered successfully.")
                st.balloons()
