import streamlit as st
import pandas as pd
import os
from datetime import date
from pathlib import Path

# Global session state for file path
if "csv_path" not in st.session_state:
    st.session_state.csv_path = None

st.set_page_config(page_title="Takaful Prospect Tracker", layout="wide")

st.title("📋 Takaful Prospect Tracker")

tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Data Source", "2️⃣ Data Input", "3️⃣ List of Data", "4️⃣ Dashboard"])

with tab1:
    st.subheader("📂 Choose Folder to Store Data")
    folder_path = st.text_input("Enter folder path (e.g., C:/Users/...):")
    if st.button("Set Folder"):
        folder = Path(folder_path)
        if folder.exists() and folder.is_dir():
            csv_file = folder / "prospect_data.csv"
            if not csv_file.exists():
                df = pd.DataFrame(columns=["Name", "Meet Date", "Plan", "Plan Price", "Commenced Date"])
                df.to_csv(csv_file, index=False)
            st.session_state.csv_path = str(csv_file)
            st.success(f"CSV will be stored at: {csv_file}")
        else:
            st.error("Invalid folder. Please check the path.")

with tab2:
    st.subheader("➕ Add New Prospect")

    if not st.session_state.csv_path:
        st.warning("Please set a valid data source in Tab 1.")
    else:
        name = st.text_input("Prospect Name")
        meet_date = st.date_input("Date Met", date.today())
        plan = st.selectbox("Plan", ["Basic", "Savings", "Education", "Critical Illness", "Retirement"])
        price = st.number_input("Plan Price (RM)", min_value=0.0)
        commenced_date = st.date_input("Date Commenced")

        if st.button("Add Prospect"):
            new_data = pd.DataFrame([{
                "Name": name,
                "Meet Date": meet_date,
                "Plan": plan,
                "Plan Price": price,
                "Commenced Date": commenced_date
            }])
            df = pd.read_csv(st.session_state.csv_path)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(st.session_state.csv_path, index=False)
            st.success("✅ Prospect added!")

with tab3:
    st.subheader("📄 List of Prospects")

    if not st.session_state.csv_path:
        st.warning("Please set a valid data source in Tab 1.")
    else:
        df = pd.read_csv(st.session_state.csv_path)
        st.dataframe(df, use_container_width=True)

with tab4:
    st.subheader("📊 Dashboard")

    if not st.session_state.csv_path:
        st.warning("Please set a valid data source in Tab 1.")
    else:
        df = pd.read_csv(st.session_state.csv_path)

        if df.empty:
            st.info("No data to display.")
        else:
            st.metric("Total Prospects", len(df))
            st.metric("Total Value (RM)", df["Plan Price"].sum())
            st.bar_chart(df["Plan"].value_counts())
