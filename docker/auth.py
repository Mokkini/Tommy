"""
Einfache Authentifizierung für KPI Dashboard
"""
import streamlit as st
import hashlib
import os

# Standard-Benutzer mit Rollen (kann über Umgebungsvariablen überschrieben werden)
# Format: {username: {"password": "...", "role": "admin|disponent"}}
DEFAULT_USERS = {
    "admin": {
        "password": os.environ.get("ADMIN_PASSWORD", "dispo2025"),
        "role": "admin"
    },
    "dispo": {
        "password": os.environ.get("USER_PASSWORD", "kpi123"),
        "role": "disponent"
    },
}

def get_user_role(username: str) -> str:
    """Gibt die Rolle eines Benutzers zurück."""
    if username in DEFAULT_USERS:
        return DEFAULT_USERS[username].get("role", "disponent")
    return "disponent"

def is_admin(username: str = None) -> bool:
    """Prüft ob der aktuelle Benutzer Admin ist."""
    if username is None:
        username = st.session_state.get("username", "")
    return get_user_role(username) == "admin"

def hash_password(password: str) -> str:
    """Hasht ein Passwort."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(username: str, password: str) -> bool:
    """Prüft Benutzername und Passwort."""
    if username in DEFAULT_USERS:
        return DEFAULT_USERS[username]["password"] == password
    return False

def login_form():
    """Zeigt das Login-Formular an."""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 KPI Dashboard Login")
        st.markdown("---")
        
        username = st.text_input("Benutzername", key="login_username")
        password = st.text_input("Passwort", type="password", key="login_password")
        
        if st.button("Anmelden", type="primary", use_container_width=True):
            if check_password(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["user_role"] = get_user_role(username)
                st.rerun()
            else:
                st.error("❌ Ungültiger Benutzername oder Passwort")
        
        st.markdown("---")
        st.caption("Bei Problemen wenden Sie sich an den Administrator.")

def logout():
    """Meldet den Benutzer ab."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["user_role"] = None
    st.rerun()

def require_auth():
    """Prüft ob Benutzer angemeldet ist, zeigt sonst Login."""
    if not st.session_state.get("authenticated", False):
        login_form()
        st.stop()
    return True

def show_user_info():
    """Zeigt Benutzerinfo in der Sidebar."""
    if st.session_state.get("authenticated", False):
        st.sidebar.markdown("---")
        role = st.session_state.get('user_role', 'disponent')
        role_display = "Administrator" if role == "admin" else "Disponent"
        st.sidebar.markdown(f"👤 **{st.session_state.get('username', 'Unbekannt')}**")
        st.sidebar.caption(f"Rolle: {role_display}")
        if st.sidebar.button("🚪 Abmelden"):
            logout()
