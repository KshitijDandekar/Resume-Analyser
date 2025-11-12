import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# --- API Key Configuration ---
# This is the only place we need to do this.
# All other pages (in the pages/ dir) will use this same config.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except (FileNotFoundError, KeyError):
    st.error("Error: `GOOGLE_API_KEY` not found in st.secrets.")
    st.info("Please add your Google AI API key to a file named `.streamlit/secrets.toml`")
    st.stop()
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()


# --- Home Page Content ---
st.title("🤖 AI Resume Analyzer")
st.markdown("Helping Recruiters and Candidates Optimize Hiring with Generative AI")

st.info(
    """
    Welcome to the AI Resume Analyzer! This tool uses generative AI to parse,
    analyze, and compare resumes.
    
    Navigate using the sidebar to the left:
    
    - **Recruiter Hub 🧑‍💼:**
        - **Batch Analysis:** Upload multiple resumes and rank them against a single job description.
        - **Side-by-Side:** Compare two resumes directly.
        - **Interview Questions:** Generate tailored questions for a candidate.
    
    - **Candidate Optimizer 🧑‍🎓:**
        - **Resume Feedback:** Upload your resume and a job description to get a match score and actionable improvement suggestions.
    """
)
