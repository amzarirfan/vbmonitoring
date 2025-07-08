import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === TITLE ===
st.title("📘 Vocabulary Saver")

# === SESSION INITIALIZATION ===
if "wordlist_unique" not in st.session_state:
    st.session_state.wordlist_unique = []

# === INPUT: Add New Word ===
new_word = st.text_input("Add a word:")
if st.button("Add to list") and new_word:
    if new_word.lower() not in [w.lower() for w in st.session_state.wordlist_unique]:
        st.session_state.wordlist_unique.append(new_word)
        st.success(f"Added: {new_word}")
    else:
        st.warning("⚠️ Word already in list.")

# === DISPLAY: Word List ===
if st.session_state.wordlist_unique:
    st.subheader("📝 Current Word List")
    df = pd.DataFrame(st.session_state.wordlist_unique, columns=["words"])
    st.dataframe(df)

    # === DOWNLOAD BUTTON ===
    output_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=output_csv,
        file_name="vocabulary.csv",
        mime="text/csv"
    )

    # === SAVE TO SPECIFIC FOLDER ===
    if st.button("💾 Save CSV to Project Folder"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vocabulary_{timestamp}.csv"

        # Fixed path
        save_path = r"C:/Users/JQ547CD/OneDrive - EY/Desktop/Self/D33 Project/APP"
        filepath = os.path.join(save_path, filename)

        try:
            df.to_csv(filepath, index=False)
            st.success(f"✅ CSV saved to: `{filepath}`")
        except Exception as e:
            st.error(f"❌ Failed to save file: {e}")
else:
    st.info("Add some words to begin.")

