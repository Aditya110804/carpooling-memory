import os
import json

# File paths for storing data
PASSENGERS_JSON = "data/passengers.json"
DRIVERS_JSON = "data/drivers.json"
BOOKINGS_JSON = "data/bookings.json"
USERS_JSON = "data/users.json"

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                content = f.read().strip()
                if not content:
                    # Empty file, return empty list
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            # Invalid JSON, treat as empty list
            return []
    return []

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Passenger functions
def load_passengers():
    return load_json(PASSENGERS_JSON)

def save_passenger(passenger_data):
    passengers = load_passengers()
    passengers.append(passenger_data)
    save_json(PASSENGERS_JSON, passengers)

# Driver functions
def load_drivers():
    return load_json(DRIVERS_JSON)

def save_driver(driver_data):
    drivers = load_drivers()
    drivers.append(driver_data)
    save_json(DRIVERS_JSON, drivers)

# User functions (for authentication)
def load_users():
    return load_json(USERS_JSON)

def save_user(user_data):
    users = load_users()
    users.append(user_data)
    save_json(USERS_JSON, users)

def username_exists(username):
    users = load_users()
    return any(user["username"] == username for user in users)

# Find matching drivers for a passenger's route (from, to, date)
def find_matches(route_info):
    drivers = load_drivers()
    matches = [
        d for d in drivers
        if d.get('from', '').strip().lower() == route_info['from'].strip().lower()
        and d.get('to', '').strip().lower() == route_info['to'].strip().lower()
        and d.get('date') == route_info['date']
    ]
    return matches

# Booking functions
def load_bookings():
    return load_json(BOOKINGS_JSON)

def save_booking(booking_data):
    bookings = load_bookings()
    bookings.append(booking_data)
    save_json(BOOKINGS_JSON, bookings)

# logic.py (add at bottom)

def update_driver_route(username, new_route):
    """
    Update only route details for a driver identified by username.
    new_route should be a dict with keys: from, to, date, time.
    """
    drivers = load_drivers()
    updated = False
    for d in drivers:
        if d["username"] == username:
            # update only the route fields
            d["from"] = new_route["from"]
            d["to"]   = new_route["to"]
            d["date"] = new_route["date"]
            d["time"] = new_route["time"]
            updated = True
            break
            if updated:
                save_json(DRIVERS_JSON, drivers)
            return updated
