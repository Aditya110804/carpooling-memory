import streamlit as st
from datetime import datetime, date, time, timedelta

def show():
    st.header("🗺️ Route Selection")

    # Get user role from session state
    role = st.session_state.get("role", None)
    if not role:
        st.warning("Please log in first.")
        st.session_state.page = "login"
        st.rerun()
        return

    # Initialize session state for route inputs
    if "from_location" not in st.session_state:
        st.session_state.from_location = ""
    if "to_location" not in st.session_state:
        st.session_state.to_location = ""
    if "route_date" not in st.session_state:
        st.session_state.route_date = datetime.today().date()
    if "route_time" not in st.session_state:
        st.session_state.route_time = datetime.now().time().replace(second=0, microsecond=0)

    # Collect route info with session state persistence
    from_location = st.text_input("From Location *", value=st.session_state.from_location)
    to_location = st.text_input("To Location *", value=st.session_state.to_location)
    date_input = st.date_input("Date *", value=st.session_state.route_date)
    selected_time = st.time_input("Preferred Time *", value=st.session_state.route_time)

    # Update session state
    st.session_state.from_location = from_location
    st.session_state.to_location = to_location
    st.session_state.route_date = date_input
    st.session_state.route_time = selected_time

    # Display nearby time options
    st.subheader("Available Time Options")
    
    # Generate time options (±2 hours in 30-min increments)
    base_time = datetime.combine(date_input, selected_time)
    time_options = []
    for offset in range(-4, 5):  # -2 hours to +2 hours in 30-min steps
        delta = timedelta(minutes=30 * offset)
        option_time = (base_time + delta).time()
        time_options.append(option_time)
    
    # Display time slots as selectable buttons
    cols = st.columns(4)
    for i, option_time in enumerate(time_options):
        with cols[i % 4]:
            if st.button(
                option_time.strftime("%I:%M %p"), 
                key=f"time_option_{i}",
                use_container_width=True
            ):
                # Update selected time when user clicks a button
                st.session_state.route_time = option_time
                st.rerun()

    if st.button("Continue"):
        if not from_location.strip() or not to_location.strip():
            st.error("Please fill in both From and To locations.")
        else:
            # Save route info in session state
            st.session_state.route_info = {
                "from": from_location.strip(),
                "to": to_location.strip(),
                "date": str(date_input),
                "time": selected_time.strftime("%H:%M:%S"),
            }
            # Redirect based on role
            if role == "passenger":
                st.session_state.page = "show_drivers"
            else:
                st.session_state.page = "driver_dashboard"
            st.rerun()

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()
