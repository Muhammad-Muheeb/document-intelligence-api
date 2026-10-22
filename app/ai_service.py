import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-3.5-flash-lite"


def ask_gemini(prompt):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    body = {
        "model": MODEL,
        "input": prompt,
    }

    response = requests.post(URL, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Gemini error {response.status_code}: {response.text}")

    data = response.json()
    for step in data["steps"]:
        if step["type"] == "model_output":
            return step["content"][0]["text"]

    raise Exception("Gemini did not return any text")

def analyze_cv_text(text):
    prompt = f"""Extract information from this CV text.
Return ONLY valid JSON, with no explanation and no markdown, in exactly this format:
{{
  "name": "",
  "role": "",
  "experience_years": 0,
  "skills": [],
  "summary": ""
}}
If something is missing, leave it empty or 0.

CV text:
{text}
"""
    answer = ask_gemini(prompt).strip()

    if answer.startswith("```"):
        answer = answer.strip("`").strip()
        if answer.startswith("json"):
            answer = answer[4:].strip()

    try:
        return json.loads(answer)
    except json.JSONDecodeError:
        raise Exception(f"Gemini did not return valid JSON: {answer}")