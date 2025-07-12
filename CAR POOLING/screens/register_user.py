import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth import save_user, username_exists

def show():
    st.header("📝 User Registration")

    with st.form("user_registration_form"):
        username = st.text_input("Choose a Username *")
        password = st.text_input("Choose a Password *", type="password")
        role = st.selectbox("Select Role *", ["passenger", "driver"])
        submitted = st.form_submit_button("Register")

        if submitted:
            if not username.strip() or not password.strip():
                st.error("Username and password cannot be empty.")
            elif username_exists(username.strip()):
                st.error("Username already exists. Please choose a different one.")
            else:
                user_data = {
                    "username": username.strip(),
                    "password": password.strip(),
                    "role": role
                }
                save_user(user_data)
                st.success(f"User '{username}' registered successfully as {role}.")
                st.balloons()

                st.session_state.username = username.strip()
                st.session_state.role = role
                st.session_state.logged_in = True

                # Redirect to role-specific profile
                if role == "driver":
                    st.session_state.page = "register_driver"  # go fill driver profile
                else:
                    st.session_state.page = "route_selection"
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Already a user? Login"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("🔙 Back to Home"):
            st.session_state.page = "home"
            st.rerun()