import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ✅ Get Desktop Path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# ✅ Streamlit App
st.title("Save Prospect Data to Desktop")

# --- Input Fields ---
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
notes = st.text_area("Additional Notes")

# --- Button to Save ---
if st.button("Save to Desktop as CSV"):
    if name and email:
        # Create DataFrame with a timestamp
        df = pd.DataFrame([{
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Notes": notes,
            "Saved_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        # File name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prospect_{timestamp}.csv"

        # Full file path on Desktop
        filepath = os.path.join(get_desktop_path(), filename)

        # Save to CSV
        df.to_csv(filepath, index=False)

        st.success(f"✅ Saved successfully to your Desktop as `{filename}`")
        st.write("📄 File path:", filepath)
    else:
        st.warning("Please enter at least a Name and Email.")
