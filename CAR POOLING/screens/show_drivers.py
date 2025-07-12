import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import find_matches, save_booking

def show():
    st.header("🚗 Available Drivers")

    passenger_route = st.session_state.get("route_info")
    if not passenger_route:
        st.warning("Please select your route first.")
        st.session_state.page = "route_selection"
        st.rerun()
        return

    matches = find_matches(passenger_route)
    if not matches:
        st.info("No matching drivers found for your route and date.")
        return

    st.success(f"Found {len(matches)} matching driver(s):")

    for idx, driver in enumerate(matches):
        with st.expander(f"Driver: {driver['name']}"):
            st.write(f"**Vehicle Number:** {driver['vehicle_no']}")
            st.write(f"**Contact:** {driver['contact']}")
            st.write(f"**Available Date & Time:** {driver['date']} {driver['time']}")

            if st.button("Book a Ride", key=f"book_{idx}"):
                booking = {
                    "passenger": {
                        "username": st.session_state.get("username"),
                        "from": passenger_route["from"],
                        "to": passenger_route["to"],
                        "date": passenger_route["date"],
                        "time": passenger_route["time"],
                    },
                    "driver": driver
                }
                save_booking(booking)
                st.success(f"Ride booked with {driver['name']}! The driver will contact you soon.")
