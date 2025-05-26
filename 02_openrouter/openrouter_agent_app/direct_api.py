# direct_api.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-small-24b-instruct-2501:free"

def run_direct_api():
    response = requests.post(
        url=f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps({
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "Hi, I have 1000 PKR, convert it to USD."
                }
            ]
        })
    )

    data = response.json()
    print("Direct API Response:")
    print(data['choices'][0]['message']['content'])

if __name__ == "__main__":
    run_direct_api()
