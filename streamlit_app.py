import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Text Summarizer", layout="centered")
st.header("📚 Text Summarizer Tool")

text_data = ""

# בחירת מקור
source = st.selectbox("Select input source:", ["Choose...", "PDF File", "Web URL"])

if source == "PDF File":
    uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded:
        try:
            pdf = PyPDF2.PdfReader(uploaded)
            text_data = "".join([page.extract_text() or "" for page in pdf.pages])
        except:
            st.error("Error reading the PDF file.")

elif source == "Web URL":
    link = st.text_input("Enter a website URL:")
    if link:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")
            text_data = "\n".join([p.get_text() for p in soup.find_all("p")])
        except:
            st.error("Failed to fetch content from the URL.")

# תצוגה וסיכום
if text_data:
    st.subheader("Extracted Text")
    st.text_area("Preview:", value=text_data[:1000], height=200)

    summary_len = st.slider("Summary length (characters):", 100, 1000, step=100, value=300)

    if st.button("Summarize"):
        st.subheader("Summary")
        st.write(text_data[:summary_len] + "...")
