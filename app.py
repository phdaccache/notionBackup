import streamlit as st
from configure import make_backup

st.title("Notion Backup")

with st.expander("See tutorial"):
    st.write("On Notion, click on the '...' icon at the top right corner of the page you want to backup and click on 'export'.")
    st.write("Make sure to export it as HTML and to mark every option:")
    st.image("image.png")
    st.write("With the zip file you just downloaded, upload it below and click on 'Make Backup'.")
    st.write("Once finished, download the new zip file and extract it where you want it.")
    st.write("To open your page locally, just click on '0.html':")
    st.image("image2.png")

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