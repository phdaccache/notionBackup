import streamlit as st
from configure import make_backup

st.title("Notion Backup")

uploaded_file = st.file_uploader("Choose a file",type="zip")

if st.button("Make Backup"):
    if uploaded_file is not None:
        with st.spinner("Making Backup"):
            make_backup(uploaded_file)
        st.success("Backup Concluded!")

    with open("Notion_Backup.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="Notion_Backup.zip",
            mime="application/zip"
        )