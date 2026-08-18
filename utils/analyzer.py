import json
import re
import google.generativeai as genai


def analyze_resume(resume_text: str, job_description: str, api_key: str, model: str = "gemini-1.5-flash") -> dict:
    """
    Sends resume and job description to Google Gemini.
    Returns a structured analysis dict with score, keywords, feedback, and rewritten bullets.
    """
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)

    prompt = f"""
You are an expert ATS (Applicant Tracking System) analyst and career coach. 
Analyze the resume below against the provided job description.

Return your analysis ONLY as a valid JSON object with EXACTLY this structure (no extra text before or after, no markdown backticks):

{{
  "match_score": <integer 0-100>,
  "score_reason": "<one sentence explaining the score>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "missing_keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>", "<keyword 4>", "<keyword 5>"],
  "weak_areas": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "rewritten_bullets": [
    {{
      "original": "<original bullet from resume>",
      "improved": "<improved version with metrics and stronger action verbs>"
    }},
    {{
      "original": "<original bullet from resume>",
      "improved": "<improved version with metrics and stronger action verbs>"
    }},
    {{
      "original": "<original bullet from resume>",
      "improved": "<improved version with metrics and stronger action verbs>"
    }}
  ],
  "overall_advice": "<2-3 sentences of overall actionable advice tailored to this specific job>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = gemini_model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if model adds them
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    # Extract JSON object
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not json_match:
        raise ValueError("Model did not return valid JSON. Please try again.")

    result = json.loads(json_match.group())
    return result