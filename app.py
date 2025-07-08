import streamlit as st
import pandas as pd

st.title("Prospect Tracker - Your Personal File")

option = st.radio(
    "Are you using this app for the first time or do you already have a CSV file?",
    ("First time - start fresh", "I have a CSV file to upload"),
)

if option == "I have a CSV file to upload":
    uploaded_file = st.file_uploader("Upload your prospects CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Please upload a CSV file to continue.")
        df = pd.DataFrame(columns=["Name", "Email", "Phone", "Status", "Notes"])
else:
    df = pd.DataFrame(columns=["Name", "Email", "Phone", "Status", "Notes"])
    st.info("Starting fresh with an empty prospects list.")

st.subheader("Your Prospects")
st.dataframe(df)  # non-editable display

# Add new prospect form
st.subheader("Add New Prospect")
with st.form("add_prospect_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    status = st.selectbox(
        "Status", ["New", "Contacted", "Interested", "Converted", "Lost"]
    )
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Prospect")

if submitted:
    if not name:
        st.error("Please enter a name for the prospect.")
    else:
        new_row = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Status": status,
            "Notes": notes,
        }
        df = df.append(new_row, ignore_index=True)
        st.success("Prospect added! Please download updated CSV.")

# Download button to export updated CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Updated CSV",
    data=csv,
    file_name="my_prospects.csv",
    mime="text/csv",
)
