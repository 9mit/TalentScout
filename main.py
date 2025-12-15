import streamlit as st
from src.database import init_db
from src import recruiter_mode, candidate_mode

# 1. App Configuration
st.set_page_config(
    page_title="CareerSuite | Professional Hiring & Prep",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize Database on Startup
init_db()

# 3. Load Custom CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# 4. Sidebar Navigation
st.sidebar.title("CareerSuite")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Select Workspace",
    ["🤖 TalentScout (Recruiter)", "🎓 PrepMaster (Candidate)", "🔒 Privacy Settings"]
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by **Google Gemini** & **Streamlit**")

# 5. Routing
if app_mode == "🤖 TalentScout (Recruiter)":
    recruiter_mode.app()
elif app_mode == "🎓 PrepMaster (Candidate)":
    candidate_mode.app()
elif app_mode == "🔒 Privacy Settings":
    from src.privacy_ui import privacy_settings_page
    privacy_settings_page()