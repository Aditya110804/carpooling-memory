# ✅ driver_route_selection.py

import streamlit as st
import sys, os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import update_driver_route, load_drivers

def show():
    st.header("🚗 Driver Route Setup")

    username = st.session_state.get("username")
    if not username:
        st.warning("Please log in as a driver.")
        st.session_state.page = "login"
        st.rerun()
        return

    # Load existing driver info
    drivers = load_drivers()
    driver = next((d for d in drivers if d.get("username") == username or d.get("driver_id") == username), None)

    with st.form("driver_route_form"):
        from_location = st.text_input("From Location *", value=driver.get("from", "") if driver else "")
        to_location = st.text_input("To Location *", value=driver.get("to", "") if driver else "")
        avail_date = st.date_input("Available Date *", value=datetime.strptime(driver.get("date"), "%Y-%m-%d").date() if driver and driver.get("date") else datetime.today())
        avail_time = st.time_input("Available Time *", value=datetime.strptime(driver.get("time"), "%H:%M:%S").time() if driver and driver.get("time") else datetime.now().time())

        submitted = st.form_submit_button("Save Route")

        if submitted:
            required_fields = [from_location, to_location]
            if any(not str(field).strip() for field in required_fields):
                st.error("Please fill all required fields marked with *.")
            else:
                new_route = {
                    "username": username,  # ✅ Added username
                    "from": from_location.strip(),
                    "to": to_location.strip(),
                    "date": str(avail_date),
                    "time": avail_time.strftime("%H:%M:%S"),
                }
                if update_driver_route(username, new_route):
                    st.success("Driver route updated successfully!")
                    st.session_state.route_info = new_route
                    st.session_state.page = "driver_dashboard"
                    st.rerun()
                else:
                    st.error("Failed to update route. Please try again.")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
