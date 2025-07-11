
import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic import load_drivers, load_bookings, update_driver_route

def show():
    st.header("🚗 Driver Dashboard")

    username = st.session_state.get("username")
    if not username:
        st.error("Session expired. Please log in again.")
        st.session_state.page = "login"
        st.rerun()
        return

    # Load driver profile
    drivers = load_drivers()
    driver = next((d for d in drivers if d.get("username") == username), None)

    if not driver:
        st.error("Something went wrong. Driver not found.")
        st.session_state.page = "login"
        st.rerun()
        return  # ❗ This was the mistake before: you had 'return' early, so nothing below was running

    ## 1) Show static profile info
    st.subheader("👤 Your Profile")
    st.write(f"**Name:** {driver.get('name', 'N/A')}")
    st.write(f"**Contact:** {driver.get('contact', 'N/A')}")
    st.write(f"**Vehicle No:** {driver.get('vehicle_no', 'N/A')}")
    st.write(f"**License No:** {driver.get('license_no', 'N/A')}")

    st.markdown("---")

    ## 2) Ride details form
    st.subheader("🗺️ Update Your Next Ride")

    # Parse default time if present, else use default
    from datetime import datetime
    default_time = driver.get("time", "09:00")
    try:
        parsed_time = datetime.strptime(default_time, "%H:%M").time()
    except ValueError:
        parsed_time = datetime.now().time()

    with st.form("ride_form"):
        from_loc = st.text_input("From", value=driver.get("from", ""))
        to_loc = st.text_input("To", value=driver.get("to", ""))
        date = st.date_input("Date", value=datetime.today().date())
        time = st.time_input("Time", value=parsed_time)
        submitted = st.form_submit_button("Save Ride Details")

        if submitted:
            new_route = {
                "from": from_loc.strip(),
                "to": to_loc.strip(),
                "date": str(date),
                "time": time.strftime("%H:%M")
            }
            if update_driver_route(username, new_route):
                st.success("✅ Ride details updated!")
                st.session_state.time_obj = time  # Store for future default
            else:
                st.error("❌ Failed to update ride. Please try again.")

    st.markdown("---")

    # 3) Show bookings
    st.subheader("📋 Your Bookings")
    bookings = load_bookings()
    your_bookings = [b for b in bookings if b["driver"].get("username") == username]

    if your_bookings:
        for b in your_bookings:
            p = b["passenger"]
            st.markdown(f"""
                **👤 Passenger:** {p.get('name', 'N/A')}  
                **📞 Contact:** {p.get('contact', 'N/A')}  
                **🛣️ Route:** {p.get('from', 'N/A')} → {p.get('to', 'N/A')}  
                **📅 When:** {p.get('date', 'N/A')} at {p.get('time', 'N/A')}
                ---
            """)
    else:
        st.info("ℹ️ No bookings yet.")