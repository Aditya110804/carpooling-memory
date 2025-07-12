import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import load_drivers, load_passengers

def show():
    st.header("👤 Profile")

    username = st.session_state.get("username")
    role = st.session_state.get("role")

    if not username or not role:
        st.warning("Please log in first.")
        st.session_state.page = "login"
        st.rerun()
        return

    if role == "driver":
        drivers = load_drivers()
        user = next((d for d in drivers if d.get("username") == username), None)
        if user:
            st.subheader("Driver Details")
            st.write(f"**Name:** {user.get('name', '')}")
            st.write(f"**Age:** {user.get('age', '')}")
            st.write(f"**Gender:** {user.get('gender', '')}")
            st.write(f"**Contact:** {user.get('contact', '')}")
            st.write(f"**Vehicle No.:** {user.get('vehicle_no', '')}")
            st.write(f"**Driver ID:** {user.get('driver_id', '')}")
            st.write(f"**National ID:** {user.get('national_id', '')}")
        else:
            st.error("Driver profile not found.")

    elif role == "passenger":
        passengers = load_passengers()
        user = next((p for p in passengers if p.get("username") == username), None)
        if user:
            st.subheader("Passenger Details")
            st.write(f"**Name:** {user.get('name', '')}")
            st.write(f"**Age:** {user.get('age', '')}")
            st.write(f"**Gender:** {user.get('gender', '')}")
            st.write(f"**Contact:** {user.get('contact', '')}")
            st.write(f"**National ID:** {user.get('national_id', '')}")
        else:
            st.error("Passenger profile not found.")

    if st.button("Back to Dashboard"):
        if role == "driver":
            st.session_state.page = "driver_dashboard"
        else:
            st.session_state.page = "route_selection"
        st.rerun()