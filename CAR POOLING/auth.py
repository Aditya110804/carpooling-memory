import json
import os

USERS_JSON = "data/users.json"

def load_users():
    if os.path.exists(USERS_JSON):
        with open(USERS_JSON, "r") as f:
            return json.load(f)
    return []

def save_user(user_data):
    users = load_users()
    users.append(user_data)
    os.makedirs(os.path.dirname(USERS_JSON), exist_ok=True)
    with open(USERS_JSON, "w") as f:
        json.dump(users, f, indent=4)
        
def username_exists(username):
    users = load_users()
    return any(user["username"] == username for user in users)
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user["role"]
    return None
