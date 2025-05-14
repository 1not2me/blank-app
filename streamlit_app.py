import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return "\n".join([p.get_text() for p in paragraphs])
    except Exception as e:
        return f"Error: {e}"

def summarize_text(text, length="short"):
    if length == "short":
        return text[:300] + "..."
    elif length == "medium":
        return text[:600] + "..."
    elif length == "detailed":
        return text[:1000] + "..."
    return text[:300] + "..."

st.set_page_config(page_title="Smart Text Summarizer", layout="centered")

st.title("📄 Smart Text Summarizer")
st.write("Choose to upload a PDF file or enter a website URL")

option = st.radio("Text source:", ["File", "URL"])

text = ""

if option == "File":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)

elif option == "URL":
    url = st.text_input("Enter a website URL:")
    if url:
        text = extract_text_from_url(url)

if text:
    st.subheader("📝 Extracted Text")
    st.text_area("Preview", value=text[:1000], height=200)

    summary_length = st.selectbox("Choose summary length:", ["short", "medium", "detailed"])
    if st.button("Generate Summary"):
        summary = summarize_text(text, summary_length)
        st.subheader("🧾 Summary")
        st.write(summary)
