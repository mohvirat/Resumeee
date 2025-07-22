
import streamlit as st
from resume_matcher import process_resumes, display_results

st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("📄 Resume Matcher – JD vs Resumes")

jd_text = st.text_area("Paste Job Description", height=200)

uploaded_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

if st.button("Analyze") and jd_text and uploaded_files:
    results = process_resumes(jd_text, uploaded_files)
    display_results(results)
