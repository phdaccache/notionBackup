import streamlit as st
import backup as bp

st.title("Notion Backup")

st.cache_data.clear()

uploaded_file = st.file_uploader("Choose a file",type="zip")

if st.button("Make Backup"):
    if uploaded_file is not None:
        with st.spinner("Making Backup"):
            t, _ = bp.time_function(bp.make_backup, uploaded_file)
        st.success("Backup Concluded! " + t)

        with open("Notion_Backup.zip", "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                file_name="Notion_Backup.zip",
                mime="application/zip"
            )

st.info("Remember to refresh the page to make another backup.")

st.write("---")

with st.expander("See tutorial"):
    st.write("On Notion, click on the '...' icon at the top right corner of the page you want to backup and click on 'export'.")
    st.write("Make sure to export it as HTML and to mark every option:")
    st.image("image.png")
    st.write("With the zip file you just downloaded, upload it below and click on 'Make Backup'.")
    st.write("Once finished, download the new zip file and extract it where you want it.")
    st.write("To open your page locally, just click on '0.html':")
    st.image("image2.png")

with st.expander("Zip too big?"):
    st.write("Download the script and run it locally!")
    st.write("Make sure you have your zipped file from Notion and the python script in the same directory, just like this:")
    st.image("image3.png")
    st.write("Then, just run the backup.py script and follow the instructions in the terminal.")
    with open("local_backup.py", "rb") as fp:
        btn = st.download_button(
            label="Download Script",
            data=fp,
            file_name="backup.py",
        )