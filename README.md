# AI Resume Analyzer

## Overview

The **AI Resume Analyzer** is an intelligent recruitment and career optimization platform built with **Streamlit** and **Google Generative AI (Gemini)**. It enables both **recruiters** and **candidates** to analyze resumes, evaluate job fit, and generate actionable insights using advanced natural language processing (NLP) and generative AI models. This application streamlines the hiring process by automating resume parsing, job description comparison, and interview question generation while offering candidates detailed feedback for improvement.


## Features

### 1. Recruiter Hub

Designed for hiring teams and HR professionals.

* **Batch Analysis:** Upload multiple resumes and evaluate them against a single job description. The system ranks candidates based on their match score.
* **Side-by-Side Comparison:** Compare two resumes directly and receive an AI-generated assessment of each candidate’s strengths, overlaps, and unique skills.
* **Interview Question Generator:** Generate categorized interview questions (behavioral, technical, and resume-specific) tailored to the candidate’s profile and the job description.

### 2. Candidate Optimizer

Built for job seekers who want to improve their resumes and increase their chances of selection.

* **Resume Feedback:** Upload your resume and a target job description to receive an AI-evaluated match score, missing keywords, and improvement suggestions.
* **Keyword Optimization:** Identify and incorporate relevant keywords from the job description to enhance resume alignment and visibility.



## System Architecture

The **AI Resume Analyzer** follows a modular architecture for scalability and maintainability.

* **Frontend:**
  Implemented using **Streamlit**, providing an interactive and user-friendly web interface for both recruiters and candidates.

* **Backend:**
  Powered by **Google Generative AI (Gemini)** models for text understanding, reasoning, and structured JSON-based data generation.
  Pydantic schemas are used to ensure consistent data validation and formatting.

* **Data Layer:**
  The system reads uploaded resume files (PDF/DOCX) directly, parses them through the Gemini model, and produces structured outputs for further comparison or feedback.



## Technology Stack

| Component       | Technology Used                           |
| --------------- | ----------------------------------------- |
| Frontend        | Streamlit                                 |
| Backend         | Python                                    |
| AI Model        | Google Gemini (via `google-generativeai`) |
| Data Validation | Pydantic                                  |
| File Handling   | Streamlit File Uploader                   |
| Deployment      | Streamlit Cloud or Local Server           |



## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/KshitijDandekar/Resume-Analyser.git
cd Resume-Analyser
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google API Key

#### Option 1: Streamlit Secrets Configuration

Create a file named `.streamlit/secrets.toml` in your project directory and add:

```toml
GOOGLE_API_KEY = "YOUR_API_KEY"
```

#### Option 2: Environment Variable (for local testing)

On macOS/Linux:

```bash
export GOOGLE_API_KEY=YOUR_API_KEY
```

On Windows:

```bash
set GOOGLE_API_KEY=YOUR_API_KEY
```



## Running the Application

After configuration, launch the Streamlit app:

```bash
streamlit run app.py
```

Once the server starts, open the provided local URL in your browser to access the application.



## Core Modules

### 1. Data Schemas (`pydantic` Models)

These models define the structured format for AI responses.

* **ParsedResume:** Extracted resume data (name, contact, education, skills, experience).
* **ComparisonResult:** Resume vs. Job Description analysis with match score, strengths, and gaps.
* **ResumeComparison:** Direct comparison of two resumes with skill overlap and recommendations.
* **ResumeFeedback:** Personalized suggestions for candidates to improve their resumes.
* **GeneratedQuestions:** AI-generated interview questions categorized as behavioral, technical, and resume-specific.

### 2. Gemini Model Configuration

All model interactions are handled via:

```python
genai.GenerativeModel(model_name="models/gemini-2.5-flash")
```

Responses are configured to return structured JSON data matching the defined Pydantic schemas.

### 3. Core Functions

* `parse_resume_from_file()`: Extracts and structures data from uploaded resumes.
* `compare_to_jd()`: Compares a parsed resume to a provided job description.
* `compare_two_resumes()`: Performs a comparative evaluation between two candidate resumes.
* `get_resume_feedback()`: Provides detailed feedback and keyword suggestions for candidates.
* `generate_interview_questions()`: Produces tailored interview questions for recruiters.


## Error Handling

The application includes robust error handling to manage:

* Missing API keys
* Invalid or unreadable resume files
* API response or parsing failures
* Streamlit configuration errors

Each error is logged and displayed with a user-friendly message.


## Example Workflow

### For Recruiters:

1. Navigate to **Recruiter Hub**.
2. Upload one or multiple resumes.
3. Paste or upload the job description.
4. View AI-generated candidate rankings, strengths, and missing areas.
5. Optionally, generate interview questions for selected candidates.

### For Candidates:

1. Go to **Candidate Optimizer**.
2. Upload your resume and paste the job description.
3. Receive a **match score**, **missing keywords**, and **improvement suggestions**.


## Future Enhancements

* Integration with Applicant Tracking Systems (ATS)
* Support for additional file formats and OCR-based text extraction
* Visualization dashboard for candidate rankings and analytics
* Resume rewriting assistance powered by Gemini
* Database storage for recruiter history and candidate profiles
