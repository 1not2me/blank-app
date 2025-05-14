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
        return f"שגיאה: {e}"

def summarize_text(text, length="קצר"):
    if length == "קצר":
        return text[:300] + "..."
    elif length == "בינוני":
        return text[:600] + "..."
    elif length == "מפורט":
        return text[:1000] + "..."
    return text[:300] + "..."

st.set_page_config(page_title="מסכם טקסטים חכם", layout="centered")

st.title("📄 אפליקציית סיכום טקסטים")
st.write("בחרי אם להעלות קובץ או להכניס קישור")

option = st.radio("מקור הטקסט:", ["קובץ", "קישור"])

text = ""

if option == "קובץ":
    uploaded_file = st.file_uploader("העלאת קובץ PDF", type=["pdf"])
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)

elif option == "קישור":
    url = st.text_input("הכניסי כתובת אתר")
    if url:
        text = extract_text_from_url(url)

if text:
    st.subheader("✏️ טקסט שחולץ")
    st.text_area("תצוגה מקדימה", value=text[:1000], height=200)

    summary_length = st.selectbox("בחרי את אורך הסיכום:", ["קצר", "בינוני", "מפורט"])
    if st.button("צור סיכום"):
        summary = summarize_text(text, summary_length)
        st.subheader("📝 סיכום")
        st.write(summary)
