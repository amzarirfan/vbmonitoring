import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Helper to get desktop path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

st.title("📘 Vocabulary Saver")

# --- Initialize session state ---
if "wordlist_unique" not in st.session_state:
    st.session_state.wordlist_unique = []

# --- Word input ---
new_word = st.text_input("Add a word:")
if st.button("Add to list") and new_word:
    if new_word not in st.session_state.wordlist_unique:
        st.session_state.wordlist_unique.append(new_word)
    else:
        st.warning("Word already in list.")

# --- Show current word list ---
if st.session_state.wordlist_unique:
    st.subheader("Current Word List")
    df = pd.DataFrame(st.session_state.wordlist_unique, columns=["words"])
    st.dataframe(df)

    # --- Download as CSV ---
    output_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", output_csv, file_name="vocabulary.csv", mime="text/csv")

    # --- Optional: Save to Desktop ---
    if st.button("💾 Save CSV to Desktop"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vocabulary_{timestamp}.csv"
        filepath = os.path.join(get_desktop_path(), filename)

        try:
            df.to_csv(filepath, index=False)
            st.success(f"CSV saved to Desktop as `{filename}`")
        except Exception as e:
            st.error(f"❌ Failed to save to Desktop: {e}")

else:
    st.info("Add some words to get started.")
