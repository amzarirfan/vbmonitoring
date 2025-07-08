import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Takaful Prospect App", layout="wide")

# --- Globals ---
if 'folder_path' not in st.session_state:
    st.session_state.folder_path = None

# --- 1. DATA SOURCE SELECTION ---
st.sidebar.header("📁 1. Select Data Folder")

base_path = Path("C:/Users/JQ547CD/OneDrive - EY/Desktop/Self/D33 Project/APP")
folder_name = st.sidebar.text_input("Folder name (e.g. July2025)", key="folder_input")

if folder_name:
    full_path = base_path / folder_name
    full_path.mkdir(parents=True, exist_ok=True)
    st.session_state.folder_path = full_path
    st.sidebar.success(f"Using folder: {full_path}")
    file_path = full_path / "prospects.csv"
else:
    st.sidebar.warning("Enter a folder name to start.")

# Exit if not selected
if not st.session_state.folder_path:
    st.stop()

# --- 2. DATA INPUT SECTION ---
st.header("📝 2. Add or Update Prospect")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Prospect Name")
        date_met = st.date_input("Date Met")
    with col2:
        plan = st.selectbox("Plan Interested", ["Family Takaful", "Medical Card", "Savings", "Retirement", "Others"])
        price = st.number_input("Plan Price (RM)", min_value=0.0, step=10.0)
    with col3:
        status = st.selectbox("Status", ["New", "Follow-up", "Closed", "Rejected"])
        date_commenced = st.date_input("Date Commenced (optional)", value=None)

    notes = st.text_area("Additional Notes")
    submitted = st.form_submit_button("💾 Save Prospect")

    if submitted and name:
        new_row = {
            "Name": name,
            "Date Met": date_met,
            "Plan": plan,
            "Price": price,
            "Status": status,
            "Date Commenced": date_commenced,
            "Notes": notes,
            "Timestamp": datetime.now()
        }

        if file_path.exists():
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])

        df.to_csv(file_path, index=False)
        st.success("Prospect saved!")

# --- 3. VIEW EXISTING DATA ---
st.header("📋 3. List of Prospects")

if file_path.exists():
    df = pd.read_csv(file_path, parse_dates=["Date Met", "Date Commenced", "Timestamp"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No data yet. Add your first prospect!")

# --- 4. DASHBOARD ---
st.header("📊 4. Dashboard Summary")

if file_path.exists() and not df.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Prospects", len(df))
    with col2:
        st.metric("Expected Income (RM)", f"{df['Price'].sum():,.2f}")
    with col3:
        closed = df[df["Status"] == "Closed"]
        st.metric("Closed Deals", len(closed))

    st.subheader("Prospects by Plan")
    st.bar_chart(df["Plan"].value_counts())

    st.subheader("Status Breakdown")
    st.bar_chart(df["Status"].value_counts())
