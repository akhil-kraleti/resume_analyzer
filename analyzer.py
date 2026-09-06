import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(text):

    prompt = f"""
You are an expert ATS (Applicant Tracking System) analyst and professional resume reviewer with 
10+ years of experience in technical recruiting and HR.

Analyze the resume below and provide a structured, actionable evaluation.

RESUME:{text}


Evaluate the resume using the following framework:

1. ATS SCORE (0-100)
   - Score based on: keyword relevance, formatting compatibility, section structure, 
     use of standard headings, and quantifiable achievements.
   - Provide a one-line justification for the score.
   - If a job description is provided, weigh keyword match against it specifically.

2. STRENGTHS (3-5 bullet points)
   - Specific, evidence-based observations (quote or reference exact resume content).
   - Focus on what makes this resume competitive.

3. WEAKNESSES (3-5 bullet points)
   - Specific gaps: missing metrics, weak action verbs, formatting issues, 
     missing keywords, unclear structure, etc.
   - Avoid generic criticism — tie each point to something concrete in the resume.

4. SUGGESTIONS (3-5 bullet points)
   - Concrete, rewritable fixes (e.g., "Change 'Responsible for team' to 
     'Led a team of 6 engineers, reducing deployment time by 30%'").
   - Prioritize the highest-impact changes first.

5. MISSING KEYWORDS (optional, only if job description provided)
   - List important keywords/skills from the job description absent in the resume.

Respond ONLY in the following JSON format, with no extra commentary:

{{
  "ats_score": <integer 0-100>,
  "score_justification": "<string>",
  "strengths": ["<string>", ...],
  "weaknesses": ["<string>", ...],
  "suggestions": ["<string>", ...],
  "missing_keywords": ["<string>", ...]
}}
"""

    response = model.generate_content(prompt)

    return response.text

def match_resume(resume_text, jd_text):

    prompt = f"""
You are an expert technical recruiter and ATS matching specialist. Your job is to evaluate 
how well a candidate's resume aligns with a specific job description, the way a hiring 
manager and an automated screening system both would.

RESUME:{resume_text}

JOB DESCRIPTION:{jd_text}

Perform a detailed comparison using the following framework:

1. MATCH SCORE (0-100%)
   - Weigh: required skills/tools match, years of experience match, education/certification 
     match, domain/industry relevance, and keyword overlap.
   - Required qualifications should count more heavily than "nice-to-have" ones.
   - Provide a one-line justification for the score.

2. MATCHING SKILLS
   - List skills/qualifications from the JD that ARE clearly present in the resume.
   - For each, briefly note where/how it's evidenced (e.g., "Python — used in 3 listed projects").

3. MISSING SKILLS
   - List required or strongly preferred skills/qualifications from the JD that are 
     NOT found in the resume.
   - Separate into "Critical" (explicitly required) vs "Preferred" (nice-to-have) if the 
     JD distinguishes them.

4. PARTIAL MATCHES (if any)
   - Skills that are implied or adjacent but not explicitly stated 
     (e.g., JD wants "AWS," resume shows "cloud infrastructure experience").

5. SUGGESTIONS
   - Specific edits to improve alignment (e.g., rephrasing, adding a missing keyword 
     the candidate likely has evidence for, reordering sections to surface relevant experience).
   - Do NOT suggest fabricating experience — only surfacing/rewording existing experience 
     or flagging real gaps to address.
   - Prioritize by expected impact on match score.

Respond ONLY in the following JSON format, with no extra commentary:

{{
  "match_score": <integer 0-100>,
  "score_justification": "<string>",
  "matching_skills": [{{"skill": "<string>", "evidence": "<string>"}}, ...],
  "missing_skills": {{
    "critical": ["<string>", ...],
    "preferred": ["<string>", ...]
  }},
  "partial_matches": [{{"jd_requirement": "<string>", "resume_evidence": "<string>"}}, ...],
  "suggestions": ["<string>", ...]
}}
"""

    response = model.generate_content(prompt)

    return response.text

def generate_questions(resume_text):

    prompt = f"""
You are an experienced technical interviewer and hiring manager preparing to interview 
this candidate. Generate interview questions that probe the specific claims, projects, 
and skills in their resume — not generic questions that could apply to anyone.

RESUME:{resume_text}



Generate interview questions across the following categories:

1. EXPERIENCE-SPECIFIC (4-6 questions)
   - Reference specific roles, projects, or achievements listed in the resume by name.
   - Probe for depth: what they actually did vs. what the team did, decisions they made, 
     trade-offs, and outcomes.
   - Example style: "You mention leading [specific project] — walk me through how you 
     approached [specific challenge]."

2. TECHNICAL / SKILL-VERIFICATION (4-6 questions)
   - Test the specific tools, languages, or methodologies listed in the resume.
   - Include at least 1-2 questions that would reveal surface-level vs. genuine expertise 
     (e.g., asking about edge cases, failure modes, or "why" not just "what").

3. GAPS & RED FLAGS (2-4 questions)
   - Politely probe any inconsistencies, employment gaps, short tenures, or vague 
     descriptions found in the resume.
   - Frame these as neutral, non-accusatory questions.

4. BEHAVIORAL (2-3 questions)
   - Based on seniority level and role type implied by the resume 
     (e.g., leadership, conflict resolution, ambiguity handling).
   - Use the STAR-friendly format (situation/task/action/result prompt).

{f'''5. ROLE-FIT (2-3 questions)
   - Directly assess alignment between resume experience and the target job description.
   - Focus especially on any gaps identified between the two.
''' if jd_text else ""}

For each question, briefly note WHY you're asking it (what it's meant to reveal).

Respond ONLY in the following JSON format, with no extra commentary:

{{
  "experience_specific": [{{"question": "<string>", "purpose": "<string>"}}, ...],
  "technical": [{{"question": "<string>", "purpose": "<string>"}}, ...],
  "gaps_red_flags": [{{"question": "<string>", "purpose": "<string>"}}, ...],
  "behavioral": [{{"question": "<string>", "purpose": "<string>"}}, ...],
  "role_fit": [{{"question": "<string>", "purpose": "<string>"}}, ...]
}}
"""

    response = model.generate_content(prompt)

    return response.text
