import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from resume_parser import extract_text
from analyzer import match_resume
from similarity import calculate_similarity

from analyzer import generate_questions



st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader( "Upload Resume", type=["pdf"])
job_description = st.text_area( "Paste Job Description")

if uploaded_file:

    text = extract_text(uploaded_file)

    if not job_description:
        st.warning("Please paste the job description.")
    elif st.button("Analyze Resume"): 
        result = match_resume(text, job_description)
        similarity_score = calculate_similarity(text,job_description)
        st.subheader("NLP Similarity Score")
        st.write(f"{similarity_score}%")
       
       
        st.markdown(result)
        questions = generate_questions(text)
        st.subheader("Interview Questions")
        st.write(questions)



