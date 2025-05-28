import os
from litellm import completion
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key
else:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

def openai():
    response = completion(
    model="openrouter/openai/gpt-4o",  # or gpt-3.5-turbo if you prefer
    messages=[{ "role": "user", "content": "Hello!" }]
)

    print(response)

def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{ "content": "Hello, how are you?", "role": "user" }]
    )
    print(response)

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{ "content": "Hello, how are you?", "role": "user" }]
    )
    print(response)

if __name__ == "__main__":
    openai()
    gemini()
    gemini2()
