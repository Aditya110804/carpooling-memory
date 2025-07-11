
import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import authenticate
from logic import load_drivers

def show():
    st.header("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login", use_container_width=True)

    st.markdown("""
    <style>
    div.stButton { display: flex; justify-content: center; }
    div.stButton > button { width: 5cm !important; }
    </style>
    """, unsafe_allow_html=True)

    if login_btn:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            role = authenticate(username, password)
            if role:
                st.success(f"Logged in as {role.capitalize()}")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role

                if role == "passenger":
                    st.session_state.page = "route_selection"
                elif role == "driver":
                    st.session_state.page = "driver_route_selection"
                    # Check if driver has already registered a route
                    if st.session_state.get("route_info"):
                        st.session_state.page = "driver_dashboard"
                else:
                    # Check if driver already registered route
                    drivers = load_drivers()
                    match = next((d for d in drivers if d.get("driver_id") == username or d.get("name") == username), None)
                    if match:
                        st.session_state.page = "driver_dashboard"
                    else:
                        st.session_state.page = "driver_route_selection"
                st.rerun()
            else:
                st.error("Invalid username or password.")

    if st.button("New user? Register here"):
        st.session_state.page = "register_user"
        st.rerun()

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
