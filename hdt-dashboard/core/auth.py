import json

USER_FILE = "users.json"
with open(USER_FILE, "r", encoding="utf-8") as f:
    user_data = json.load(f)

current_user = None

def authenticate_user(username, password):
    """Simple authentication based on users.json"""
    global current_user
    for user in user_data.get("users", []):
        if user["username"] == username and user["password"] == password:
            current_user = username
            return True
    return False

def login(username, password):
    return authenticate_user(username, password)

def get_current_user():
    global current_user
    return current_user
