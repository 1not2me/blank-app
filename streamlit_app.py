import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Text Summarizer", layout="centered")
st.header("🌐 Web Page Summarizer")

text_data = ""

url = st.text_input("הדביקי כאן קישור לאתר (URL):")

if url:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text_data = "\n".join(p.get_text() for p in paragraphs)
    except Exception as e:
        st.error(f"שגיאה: {e}")

if text_data:
    st.subheader("✏️ טקסט שחולץ מהאתר:")
    st.text_area("תצוגה מקדימה", value=text_data[:1000], height=200)

    length = st.slider("בחרי את אורך הסיכום (תווים):", 100, 1000, 300)
    if st.button("צור סיכום"):
        st.subheader("📝 סיכום")
        st.write(text_data[:length] + "...")
