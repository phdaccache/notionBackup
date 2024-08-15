import streamlit as st
import backup as bp

st.title("Notion Backup")

st.subheader("Tutorial")
st.write("On Notion, click on the '...' icon at the top right corner of the page you want to backup and click on 'export'.")
st.write("Make sure to export it as HTML and to mark every option:")
st.image("image.png")
st.write("Now, you have to download the python script and run it locally.")
st.write("Make sure you have your zipped file from Notion and the python script in the same directory, just like this:")
st.image("image3.png")
st.write("Then, just run the backup.py script and follow the instructions in the terminal.")
st.write("To open your page locally, just click on '0.html':")
st.image("image2.png")

st.write("---")

with open("backup.py", "rb") as fp:
    btn = st.download_button(
        label="Download Script",
        data=fp,
        file_name="backup.py",
    )