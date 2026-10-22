import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/interactions"
headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key,
}
body = {
        "model": "gemini-3.5-flash-lite",
    "input": "Say hello in one short sentence",
}

response = requests.post(url, headers=headers, json=body)
data = response.json()

for step in data["steps"]:
    if step["type"] == "model_output":
        print(step["content"][0]["text"])