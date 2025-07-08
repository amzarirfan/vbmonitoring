import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Get desktop path (cross-platform)
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# 2. Streamlit App
st.title("Save CSV to Desktop")

# Input fields
name = st.text_input("Enter Name")
email = st.text_input("Enter Email")
age = st.number_input("Enter Age", min_value=0, max_value=120, step=1)

# Button to save
if st.button("Save to Desktop CSV"):
    if name and email:
        # Create dataframe
        df = pd.DataFrame([[name, email, age]], columns=["Name", "Email", "Age"])
        
        # Generate file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_data_{timestamp}.csv"
        filepath = os.path.join(get_desktop_path(), filename)

        # Save to desktop
        df.to_csv(filepath, index=False)

        st.success(f"Saved successfully to Desktop as '{filename}'")
    else:
        st.warning("Please enter both name and email.")
