from app.ai_service import analyze_cv_text

sample_cv = """
John Smith
Python Developer
3 years of experience building REST APIs with FastAPI and PostgreSQL.
Skills: Python, FastAPI, PostgreSQL, Docker, Git
"""

result = analyze_cv_text(sample_cv)
print(result)
print(result["name"])
print(result["skills"])