import streamlit as st
from utils import (
    parse_resume_from_file, 
    compare_to_jd, 
    compare_two_resumes, 
    generate_interview_questions
)
import pandas as pd

st.set_page_config(page_title="Recruiter Hub", page_icon="🧑‍💼", layout="wide")
st.title("Recruiter Hub 🧑‍💼")

# Initialize session state
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = []

# --- 1. BATCH RANKING (FEATURE 1) ---
st.header("Batch Resume Ranking")
st.info("Upload multiple resumes and one job description to rank all candidates.")

jd_text_batch = st.text_area("Paste Job Description Here", key="jd_batch", height=200)
uploaded_resumes_batch = st.file_uploader(
    "Upload Candidate Resumes (PDF, DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    key="resumes_batch"
)

if st.button("Rank All Candidates", type="primary", disabled=(not jd_text_batch or not uploaded_resumes_batch)):
    st.session_state.batch_results = []
    
    # Parse and compare each resume
    progress_bar = st.progress(0, "Analyzing resumes...")
    for i, file in enumerate(uploaded_resumes_batch):
        parsed_resume = parse_resume_from_file(file)
        if parsed_resume:
            comparison = compare_to_jd(parsed_resume, jd_text_batch)
            if comparison:
                st.session_state.batch_results.append(comparison)
        progress_bar.progress((i + 1) / len(uploaded_resumes_batch), f"Analyzing {file.name}...")
    
    progress_bar.empty()

# Display ranked results
if st.session_state.batch_results:
    st.subheader("Ranked Candidate List")
    
    # Sort results by match score
    sorted_results = sorted(st.session_state.batch_results, key=lambda x: x.match_score, reverse=True)
    
    # Create a clean DataFrame for display
    display_data = []
    for i, res in enumerate(sorted_results):
        display_data.append({
            "Rank": i + 1,
            "Name": res.name,
            "Score": f"{res.match_score}%",
            "Summary": res.summary
        })
    
    st.dataframe(pd.DataFrame(display_data), use_container_width=True)

    # --- 1b. INTERVIEW QUESTIONS (FEATURE 2) ---
    st.subheader("Generate Interview Questions")
    st.info("Select a top candidate to generate tailored interview questions.")
    
    # Create a selectbox with candidate names
    candidate_names = [res.name for res in sorted_results]
    selected_name = st.selectbox("Select Candidate", options=candidate_names)
    
    if st.button("Generate Questions"):
        # Find the selected candidate's parsed resume
        selected_resume_obj = None
        for res in sorted_results:
            if res.name == selected_name:
                # This is a hacky way; ideally, we'd store the ParsedResume obj
                # For now, let's re-parse (but @st.cache_data will save us)
                # A better way: store (name, parsed_resume) in a dict
                for file in uploaded_resumes_batch:
                    if parse_resume_from_file(file).name == selected_name:
                         selected_resume_obj = parse_resume_from_file(file)
                         break
                break
        
        if selected_resume_obj:
            questions = generate_interview_questions(selected_resume_obj, jd_text_batch)
            if questions:
                st.markdown("#### Behavioral Questions")
                for q in questions.behavioral:
                    st.markdown(f"- **Q:** {q.question}\n  - *Reasoning: {q.reasoning}*")
                
                st.markdown("#### Technical Questions")
                for q in questions.technical:
                    st.markdown(f"- **Q:** {q.question}\n  - *Reasoning: {q.reasoning}*")
                
                st.markdown("#### Resume-Specific Questions")
                for q in questions.resume_specific:
                    st.markdown(f"- **Q:** {q.question}\n  - *Reasoning: {q.reasoning}*")

st.divider()

# --- 2. SIDE-BY-SIDE COMPARISON (FEATURE 3) ---
st.header("Side-by-Side Candidate Comparison")
col1, col2 = st.columns(2)

with col1:
    resume_a_file = st.file_uploader("Upload Resume A", type=["pdf", "docx"], key="resume_a")
with col2:
    resume_b_file = st.file_uploader("Upload Resume B", type=["pdf", "docx"], key="resume_b")

if st.button("Compare Resumes", disabled=(not resume_a_file or not resume_b_file)):
    resume_a = parse_resume_from_file(resume_a_file)
    resume_b = parse_resume_from_file(resume_b_file)
    
    if resume_a and resume_b:
        comparison = compare_two_resumes(resume_a, resume_b)
        if comparison:
            st.subheader(f"Comparison: {resume_a.name} vs. {resume_b.name}")
            
            st.markdown("#### 💬 Recommendation")
            st.write(comparison.recommendation)

            st.markdown("#### 🤝 Skill Overlap")
            st.write(", ".join(comparison.skill_overlap))
            
            # Display strengths side-by-side
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"#### ✅ Unique Strengths ({resume_a.name})")
                for item in comparison.candidate_a_strengths:
                    st.markdown(f"- {item}")
            with c2:
                st.markdown(f"#### ✅ Unique Strengths ({resume_b.name})")
                for item in comparison.candidate_b_strengths:
                    st.markdown(f"- {item}")
