
import streamlit as st
import fitz  # PyMuPDF
import re

ESSENTIAL_SKILLS = [
    "c#", ".net", "asp.net", "angular", "api", "rest", "azure", "entity framework", 
    "sql", "linq", "javascript", "html", "css"
]
PREFERRED_SKILLS = [
    "openai", "chatgpt", "langchain", "genai", "ai", "ml", "tensorflow", "fastapi", 
    "copilot", "azure devops", "docker", "microservices", "communication", "remote"
]

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

def skill_match(text, skills):
    matches = [skill for skill in skills if skill in text]
    return matches, len(matches) / len(skills) * 100 if skills else 0

def get_strengths(text):
    strengths = []
    if "openai" in text or "chatgpt" in text: strengths.append("GenAI / NLP experience")
    if "azure" in text or "aws" in text: strengths.append("Cloud exposure")
    if "remote" in text: strengths.append("Remote work experience")
    if "communication" in text or "client" in text: strengths.append("Client communication skills")
    if "langchain" in text: strengths.append("LangChain experience")
    if "tensorflow" in text: strengths.append("TensorFlow / ML")
    return ", ".join(strengths) if strengths else "General .NET/Angular expertise"

def get_weaknesses(text):
    weaknesses = []
    if not any(skill in text for skill in ["chatgpt", "openai", "genai"]): weaknesses.append("Missing direct GenAI evidence")
    if "communication" not in text: weaknesses.append("No strong communication emphasis")
    if "certification" not in text: weaknesses.append("No AI-related certifications mentioned")
    return ", ".join(weaknesses) if weaknesses else "None noted"

def process_resumes(jd_text, uploaded_files):
    results = []
    for file in uploaded_files:
        name = file.name.replace("_", " ").split(".")[0]
        text = extract_text_from_pdf(file)

        essential, essential_pct = skill_match(text, ESSENTIAL_SKILLS)
        preferred, preferred_pct = skill_match(text, PREFERRED_SKILLS)

        strengths = get_strengths(text)
        weaknesses = get_weaknesses(text)

        total_score = round((essential_pct * 0.7 + preferred_pct * 0.3), 2)
        level = "✅ Green" if total_score > 80 else ("⚠️ Yellow" if total_score >= 60 else "❌ Red")

        results.append({
            "Candidate": name,
            "Essential Match %": f"{round(essential_pct)}%",
            "Preferred Match %": f"{round(preferred_pct)}%",
            "Match Level": level,
            "Score": total_score,
            "Strengths": strengths,
            "Weaknesses": weaknesses
        })
    return sorted(results, key=lambda x: x["Score"], reverse=True)

def display_results(results):
    st.markdown("### 🔍 Analysis Results")
    st.dataframe([
        {
            "Candidate": r["Candidate"],
            "% Match – Required Skills": r["Essential Match %"],
            "% Match – Preferred Skills": r["Preferred Match %"],
            "Strengths": r["Strengths"],
            "Weaknesses": r["Weaknesses"]
        } for r in results
    ])
