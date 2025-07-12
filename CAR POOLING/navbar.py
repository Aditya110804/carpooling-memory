import streamlit as st

def render_navbar():
    if "username" not in st.session_state or "role" not in st.session_state:
        return  # don't show navbar if user not logged in

    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "")

    st.markdown("""
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 1rem;
            background-color: #004466;
            color: white;
            font-size: 16px;
        }
        .navbar-left {
            font-weight: bold;
            font-size: 18px;
        }
        .navbar-right {
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }
        .navbar-link {
            color: white;
            text-decoration: none;
            font-weight: normal;
            cursor: pointer;
        }
    </style>
    <div class="navbar">
        <div class="navbar-left">🚗 Smart Ride Pooling</div>
        <div class="navbar-right">
            <span class="navbar-link">👤 {username} ({role})</span>
            <span class="navbar-link" onclick="window.location.href='/?nav=profile'">Profile</span>
            <span class="navbar-link" onclick="window.location.href='/?nav=logout'">Logout</span>
        </div>
    </div>
    """.format(username=username, role=role.capitalize()), unsafe_allow_html=True)

    # Handle manual route switch
    query_params = st.experimental_get_query_params()
    if "nav" in query_params:
        nav_target = query_params["nav"][0]
        if nav_target == "logout":
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.session_state.username = None
            st.session_state.role = None
            st.experimental_set_query_params()  # clear
            st.rerun()
        elif nav_target == "profile":
            st.session_state.page = "profile"
            st.experimental_set_query_params()  # clear
            st.rerun()