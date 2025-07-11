import streamlit as st
import base64
import sys, os
from PIL import Image

# Import your page modules
from screens import (
    home,
    login,
    route_selection,
    show_drivers,
    driver_dashboard,
    register_user,
    driver_route_selection,  # ✅ new import
)
from logic import load_drivers  # ✅ for checking if driver exists

# Background image setup
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;
        }}
        .css-1d391kg {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 10px;
            padding: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("static/images/background.png")

st.set_page_config(
    page_title="Smart Ride Pooling",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Session state init
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'route_info' not in st.session_state:
        st.session_state.route_info = None

    # Navigation logic
    if st.session_state.page == 'home':
        home.show()

    elif st.session_state.page == 'login':
        login.show()

    elif st.session_state.page == 'register_user':
        register_user.show()

    elif st.session_state.page == 'route_selection':
        route_selection.show()

    elif st.session_state.page == 'driver_route_selection':
        driver_route_selection.show()

    elif st.session_state.page == 'show_drivers':
        show_drivers.show()

    elif st.session_state.page == 'driver_dashboard':
        driver_dashboard.show()

    # Logout logic
    if st.session_state.logged_in:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.route_info = None
            st.session_state.page = 'home'
            st.rerun()

    # Car animation
    with open("static/images/car.png", "rb") as img_file:
        img_bytes = img_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()
        img_data_url = f"data:image/png;base64,{img_base64}"

    st.markdown(f"""
    <style>
    .car-animation-container {{
        position: fixed;
        left: 0;
        bottom: 5px;
        width: 150vw;
        height: 150px;
        pointer-events: none;
        z-index: 9999;
    }}
    .car-animation-img {{
        position: absolute;
        left: -200px;
        bottom: 0;
        height: 100px;
        animation: moveCar 7s linear infinite;
    }}
    @keyframes moveCar {{
        0% {{ left: -200px; }}
        100% {{ left: 100vw; }}
    }}
    </style>
    <div class="car-animation-container">
        <img src="{img_data_url}" class="car-animation-img" alt="Car">
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()