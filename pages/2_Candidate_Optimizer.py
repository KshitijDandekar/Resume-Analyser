import streamlit as st
from utils import parse_resume_from_file, get_resume_feedback

st.set_page_config(page_title="Candidate Optimizer", page_icon="🧑‍🎓", layout="wide")
st.title("Candidate Optimizer 🧑‍🎓")
st.info("Upload your resume and a job description to get actionable feedback!")

# --- 1. UI FOR UPLOADS ---
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_resume = st.file_uploader(
        "Upload Your Resume",
        type=["pdf", "docx"],
        key="candidate_resume"
    )

with col2:
    jd_text = st.text_area(
        "Paste the Job Description You're Targeting",
        height=300,
        key="candidate_jd"
    )

if st.button("Analyze My Resume", type="primary", disabled=(not uploaded_resume or not jd_text)):
    parsed_resume = parse_resume_from_file(uploaded_resume)
    
    if parsed_resume:
        feedback = get_resume_feedback(parsed_resume, jd_text)
        
        if feedback:
            st.subheader("📊 Your Analysis")
            st.metric("Overall Match Score", f"{feedback.match_score}%")
            
            st.divider()
            
            st.markdown("#### 💡 Improvement Suggestions")
            st.warning("Use these suggestions to rephrase your experience and skills.")
            for item in feedback.improvement_suggestions:
                st.markdown(f"- {item}")
                
            st.divider()
            
            st.markdown("#### 🔑 Missing Keywords from Job Description")
            st.info("Try to naturally include these keywords in your resume if you have the experience.")
            # Display as pills/tags
            st.write(", ".join(f"`{keyword}`" for keyword in feedback.keyword_opportunities))
            
            with st.expander("Show My Parsed Resume Data"):
                st.json(parsed_resume.model_dump_json(indent=2))
