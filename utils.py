import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# --- 1. PYDANTIC SCHEMAS (DATA CONTRACTS) ---

class Education(BaseModel):
    """Represents a single education entry."""
    degree: Optional[str] = Field(description="e.g., M.S. in Computer Science")
    university: Optional[str] = Field(description="e.g., AI University")
    graduation_year: Optional[str] = Field(description="e.g., 2024")

class Experience(BaseModel):
    """Represents a single work experience entry."""
    title: Optional[str] = Field(description="e.g., Senior Software Engineer")
    company: Optional[str] = Field(description="e.g., Tech Innovations Inc.")
    duration: Optional[str] = Field(description="e.g., 2022-Present")
    description: Optional[str] = Field(description="Key responsibilities")

class ParsedResume(BaseModel):
    """The main structured model for a parsed resume."""
    name: Optional[str] = Field(description="Full name")
    email: Optional[str]
    phone: Optional[str]
    summary: Optional[str] = Field(description="Professional summary")
    skills: List[str] = Field(description="List of skills")
    education: List[Education]
    experience: List[Experience]

class ComparisonResult(BaseModel):
    """(Recruiter) Output for Resume vs. JD comparison."""
    name: str = Field(description="Candidate's full name")
    match_score: int = Field(description="Percentage from 0-100 of the match")
    summary: str = Field(description="One-paragraph summary of candidate's fit")
    strengths: List[str] = Field(description="Key skills/experiences that match")
    gaps: List[str] = Field(description="Key requirements missing from resume")
    
class ResumeComparison(BaseModel):
    """(Recruiter) Output for Resume A vs. Resume B comparison."""
    skill_overlap: List[str] = Field(description="Skills both candidates possess")
    candidate_a_strengths: List[str] = Field(description="Unique strengths of Candidate A")
    candidate_b_strengths: List[str] = Field(description="Unique strengths of Candidate B")
    recommendation: str = Field(description="Brief recommendation on who is stronger")

class ResumeFeedback(BaseModel):
    """(Candidate) Output for Resume vs. JD feedback."""
    match_score: int = Field(description="Percentage from 0-100 of the match")
    keyword_opportunities: List[str] = Field(description="Keywords from the JD missing in the resume")
    improvement_suggestions: List[str] = Field(description="Actionable suggestions for how to rephrase resume sections")

class InterviewQuestion(BaseModel):
    """(Recruiter) A single generated interview question."""
    question: str = Field(description="The specific question")
    reasoning: str = Field(description="Why this question is being asked")

class GeneratedQuestions(BaseModel):
    """(Recruiter) Full list of generated questions."""
    behavioral: List[InterviewQuestion]
    technical: List[InterviewQuestion]
    resume_specific: List[InterviewQuestion]


# --- 2. GEMINI API HELPER FUNCTIONS ---

def get_gemini_model(schema, model_name="models/gemini-2.5-flash"):
    """Configures and returns a Gemini model in JSON mode."""
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=schema 
    )
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config
    )

@st.cache_data(show_spinner="Parsing Resume...")
def parse_resume_from_file(uploaded_file):
    """Sends resume bytes to Gemini and returns a ParsedResume object."""
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        resume_file_part = {"mime_type": uploaded_file.type, "data": bytes_data}
        prompt = [
            "You are an expert resume parser. Extract all information from the provided resume file.",
            "Parse the document and return the data in the requested JSON format.",
            resume_file_part
        ]
        try:
            model = get_gemini_model(ParsedResume)
            response = model.generate_content(prompt)
            return ParsedResume.model_validate_json(response.text)
        except Exception as e:
            st.error(f"Error parsing resume '{uploaded_file.name}': {e}")
            return None
    return None

@st.cache_data(show_spinner="Analyzing Resume vs. JD...")
def compare_to_jd(resume_object: ParsedResume, jd_text: str):
    """(Recruiter) Compares a resume to a JD and returns ComparisonResult."""
    resume_json_string = resume_object.model_dump_json(indent=2)
    prompt = f"""
    You are an expert hiring manager. Analyze the provided candidate's resume against the job description.
    Use the candidate's name from the resume.
    
    JOB DESCRIPTION:
    ---
    {jd_text}
    ---
    
    CANDIDATE'S RESUME (JSON):
    ---
    {resume_json_string}
    ---
    
    Provide a detailed analysis in the required JSON format.
    """
    try:
        model = get_gemini_model(ComparisonResult) 
        response = model.generate_content(prompt)
        return ComparisonResult.model_validate_json(response.text)
    except Exception as e:
        st.error(f"Error during comparison: {e}")
        return None

@st.cache_data(show_spinner="Comparing Resumes...")
def compare_two_resumes(resume_a: ParsedResume, resume_b: ParsedResume):
    """(Recruiter) Compares two resumes and returns ResumeComparison."""
    resume_a_json = resume_a.model_dump_json(indent=2)
    resume_b_json = resume_b.model_dump_json(indent=2)
    prompt = f"""
    You are an expert HR manager. Compare two candidates.
    
    CANDIDATE A'S RESUME (JSON):
    ---
    {resume_a_json}
    ---
    
    CANDIDATE B'S RESUME (JSON):
    ---
    {resume_b_json}
    ---
    
    Provide a concise, side-by-side comparison in the required JSON format.
    """
    try:
        model = get_gemini_model(ResumeComparison)
        response = model.generate_content(prompt)
        return ResumeComparison.model_validate_json(response.text)
    except Exception as e:
        st.error(f"Error during resume comparison: {e}")
        return None

@st.cache_data(show_spinner="Generating Feedback...")
def get_resume_feedback(resume_object: ParsedResume, jd_text: str):
    """(Candidate) Compares resume to JD and returns ResumeFeedback."""
    resume_json_string = resume_object.model_dump_json(indent=2)
    prompt = f"""
    You are a friendly and encouraging career coach. 
    Analyze the provided resume against the job description.
    
    JOB DESCRIPTION:
    ---
    {jd_text}
    ---
    
    MY RESUME (JSON):
    ---
    {resume_json_string}
    ---
    
    Provide a match score, list missing keywords, and give actionable 
    improvement suggestions on how I can rephrase my experience to 
    better match the job description.
    Return your analysis in the required JSON format.
    """
    try:
        model = get_gemini_model(ResumeFeedback) 
        response = model.generate_content(prompt)
        return ResumeFeedback.model_validate_json(response.text)
    except Exception as e:
        st.error(f"Error generating feedback: {e}")
        return None

@st.cache_data(show_spinner="Generating Interview Questions...")
def generate_interview_questions(resume_object: ParsedResume, jd_text: str):
    """(Recruiter) Generates interview questions."""
    resume_json_string = resume_object.model_dump_json(indent=2)
    prompt = f"""
    You are a senior hiring manager. Based on the resume and job description, 
    generate 3 behavioral, 3 technical, and 3 resume-specific questions.
    The 'resume_specific' questions should probe deeper into the candidate's 
    listed projects or job history.
    
    JOB DESCRIPTION:
    ---
    {jd_text}
    ---
    
    CANDIDATE'S RESUME (JSON):
    ---
    {resume_json_string}
    ---
    
    Return your questions in the required JSON format.
    """
    try:
        model = get_gemini_model(GeneratedQuestions) 
        response = model.generate_content(prompt)
        return GeneratedQuestions.model_validate_json(response.text)
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return None
