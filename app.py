import streamlit as st
from datetime import date

# App config
st.set_page_config(
    page_title="Takaful Prospect Tracker",
    page_icon="🛡️",
    layout="centered",
)

# Initialize session data
if "prospects" not in st.session_state:
    st.session_state.prospects = []

# Sidebar Navigation
page = st.sidebar.radio("📋 Navigate", ["Add Prospect", "Dashboard"])

# ---------------------- PAGE: ADD PROSPECT ----------------------
if page == "Add Prospect":
    st.title("➕ Add New Prospect")

    with st.form("prospect_form", clear_on_submit=False):
        name = st.text_input("👤 Prospect Name")
        meeting_date = st.date_input("📅 Date Met", value=date.today())
        plan = st.selectbox("📦 Plan Interested", ["Life Takaful", "Medical", "Education", "Investment", "Other"])
        plan_price = st.number_input("💰 Plan Price (RM)", min_value=0.0, step=10.0)
        status = st.selectbox("📌 Status", ["New", "Follow-up", "In Progress", "Closed - Success", "Closed - Lost"])
        commence_date = st.date_input("🗓️ Plan Commencement Date (optional)", value=None)

        submitted = st.form_submit_button("💾 Save Prospect")

        if submitted:
            st.session_state.prospects.append({
                "name": name,
                "meeting_date": meeting_date,
                "plan": plan,
                "plan_price": plan_price,
                "status": status,
                "commence_date": commence_date if commence_date != date.today() else None,
            })
            st.success(f"Prospect '{name}' saved!")

# ---------------------- PAGE: DASHBOARD ----------------------
elif page == "Dashboard":
    st.title("📊 Prospect Dashboard")

    if not st.session_state.prospects:
        st.info("No prospects added yet. Go to 'Add Prospect' to start.")
    else:
        st.write("### All Prospects")
        for i, p in enumerate(st.session_state.prospects):
            with st.expander(f"{p['name']} - {p['plan']} ({p['status']})"):
                st.write(f"📅 Met on: {p['meeting_date']}")
                st.write(f"💰 Plan Price: RM {p['plan_price']}")
                st.write(f"🗓️ Start Date: {p['commence_date'] if p['commence_date'] else 'Not Set'}")
                st.write(f"📌 Status: {p['status']}")
