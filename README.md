AI Resume Analyzer

This is a multi-page Streamlit application that uses the Google Gemini API to parse, analyze, and compare resumes.

It features two modes:

Recruiter Hub: For batch-processing resumes, ranking them against a job description, comparing candidates, and generating interview questions.

Candidate Optimizer: For job seekers to analyze their resume against a job description and get actionable feedback for improvement.

How to Run

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)


Install dependencies:

pip install -r requirements.txt


Set your API Key:

Add your Google AI API key to the .streamlit/secrets.toml file.

Run the app:

streamlit run app.py
