import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Takaful Prospect Tracker", layout="centered")

# 🔍 Choose data directory
default_dir = os.getcwd()
folder_path = st.text_input("📁 Enter Folder to Store Data", value=default_dir)
csv_file = os.path.join(folder_path, "prospects.csv")

def load_data():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=["Name", "Date Met", "Plan", "Plan Price", "Status", "Commenced Date"])

def save_data(df):
    os.makedirs(folder_path, exist_ok=True)
    df.to_csv(csv_file, index=False)

# 🧭 Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Add Prospect", "Dashboard"])

# 📦 Load data
df = load_data()

if menu == "Add Prospect":
    st.title("📝 Add New Prospect")

    name = st.text_input("Name")
    date_met = st.date_input("Date Met")
    plan = st.text_input("Plan")
    plan_price = st.number_input("Plan Price", min_value=0.0, step=0.01)
    status = st.selectbox("Status", ["New", "Interested", "Signed", "Not Interested"])
    commenced_date = st.date_input("Commenced Date (if any)", disabled=(status != "Signed"))

    if st.button("Save Prospect"):
        new_data = pd.DataFrame([{
            "Name": name,
            "Date Met": date_met,
            "Plan": plan,
            "Plan Price": plan_price,
            "Status": status,
            "Commenced Date": commenced_date if status == "Signed" else None
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success(f"Prospect '{name}' saved successfully!")

elif menu == "Dashboard":
    st.title("📊 Prospect Dashboard")

    if df.empty:
        st.info("No prospects yet.")
    else:
        st.dataframe(df)
        st.write("### 🔢 Total Prospects by Status")
        st.bar_chart(df["Status"].value_counts())
