import os
import streamlit as st
import pdfplumber
from groq import Groq
client = Groq()

st.set_page_config(page_title="LLMatch", layout="centered")

st.image("llmatch_logo.png", width=200)
st.title("LLMatch")
st.subheader("Smart Resume Matching using LLMs")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        st.success("Resume text extracted!")
        st.text_area("Extracted Resume Text", resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text, height=200)
    except Exception as e:
        st.error(f"Error: {e}")

job_desc = st.text_area("Paste the job description here:", height=150)

def analyze_skills(text):
    prompt = f"List the candidate’s key skills and strengths based on the resume:\n{text}"
    r = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}], max_tokens=200)
    return r.choices[0].message.content.strip()

def evaluate_job_fit(text, jd):
    prompt = f"Evaluate how well this resume matches the job description. Give a fit score (1-10), strengths, and gaps.\nResume:\n{text}\nJob:\n{jd}"
    r = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}], max_tokens=300)
    return r.choices[0].message.content.strip()

def suggest_improvements(text, jd):
    prompt = f"Suggest 3 improvements to this resume based on the job description.\nResume:\n{text}\nJob:\n{jd}"
    r = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}], max_tokens=250)
    return r.choices[0].message.content.strip()

if st.button("Analyze"):
    if not resume_text:
        st.warning("Please upload a resume.")
    elif not job_desc.strip():
        st.warning("Please paste the job description.")
    else:
        with st.spinner("Analyzing..."):
            st.subheader("Skill Summary")
            st.write(analyze_skills(resume_text))

            st.subheader("Job Match Analysis")
            st.write(evaluate_job_fit(resume_text, job_desc))

            st.subheader("Improvement Suggestions")
            st.write(suggest_improvements(resume_text, job_desc))


# --- Footer Section ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 14px;'>
        Built with ❤️ by <strong>Pranav</strong> · 
        <a href='https://github.com/pranavcodesofficial' target='_blank'>GitHub</a> · 
        <a href='https://linkedin.com/in/pranavcodes' target='_blank'>LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)