import sys
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["GEMINI_API_KEY"] = "your-gemini-api-key"

def openai():
    response = completion(
        model="openai/gpt-4o",
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response)

def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response)

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "openai":
        openai()
    elif cmd == "gemini":
        gemini()
    elif cmd == "gemini2":
        gemini2()
    else:
        print("Usage: uv run <openai|gemini|gemini2>")
