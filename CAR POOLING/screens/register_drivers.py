import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import save_driver

def show():
    st.header("🚗 Driver Registration")

    with st.form("driver_form"):
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=21, max_value=70)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        driver_id = st.text_input("Driver ID *")
        vehicle_no = st.text_input("Vehicle Number *")
        license_no = st.text_input("Driving License Number *")
        contact = st.text_input("Contact Number *")
        from_location = st.text_input("From Location *")
        to_location = st.text_input("To Location *")
        avail_date = st.date_input("Available Date *")
        avail_time = st.time_input("Available Time *")

        submitted = st.form_submit_button("Register")

        required_fields = [name, driver_id, vehicle_no, license_no, contact, from_location, to_location]
        if submitted:
            if any(not str(field).strip() for field in required_fields):
                st.error("Please fill all required fields marked with *.")
            else:
                driver_data = {
                    "name": name.strip(),
                    "age": int(age),
                    "gender": gender,
                    "driver_id": driver_id.strip(),
                    "vehicle_no": vehicle_no.strip(),
                    "license_no": license_no.strip(),
                    "contact": contact.strip(),
                    "from": from_location.strip(),
                    "to": to_location.strip(),
                    "date": str(avail_date),
                    "time": avail_time.strftime("%H:%M:%S"),
                }
                save_driver(driver_data)
                st.success(f"Thank you {name}! Driver registered successfully.")
                st.balloons()
