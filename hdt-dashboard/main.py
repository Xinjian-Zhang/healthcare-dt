import eel
from core.auth import login, get_current_user
from core.data_retrieval import fetch_dashboard_data
from core.ai_suggestion import get_ai_suggestion

# Initialize Eel frontend
eel.init("web")

# Expose functions to JS
eel.expose(login)
eel.expose(get_current_user)
eel.expose(fetch_dashboard_data)
eel.expose(get_ai_suggestion)

def start_app():
    eel.start("login.html", size=(600, 400))

if __name__ == "__main__":
    start_app()
