# 🧠 OpenRouter AI Agents Project

This project demonstrates two ways to interact with OpenRouter's API:

1. **Direct API** usage with `requests`
2. **OpenAI Agents SDK** with `openai-agents`

---

## 📁 Project Structure

openai-agent-app/
│
├── .env # Stores API key (not tracked by Git)
├── requirements.txt # Required Python packages
├── direct_api.py # Direct OpenRouter API call
├── openai_sdk_agent.py # OpenAI Agents SDK usage
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🔐 Environment Setup

### 1. Create a `.env` file

Create a `.env` file in the root folder with this content:

OPENROUTER_API_KEY=your_actual_openrouter_api_key

yaml
Copy
Edit

> ⚠️ Do not share your `.env` file or push it to GitHub.

---

## 🧪 Virtual Environment Setup

### 1. Create & activate virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🚀 Run Scripts
🟦 Direct API call
bash
Copy
Edit
python direct_api.py
This script sends a prompt directly to OpenRouter and prints the result.

🟩 OpenAI Agents SDK
bash
Copy
Edit
python openai_sdk_agent.py
This script creates an AI agent using OpenAI’s agent SDK and prints its output.

📦 requirements.txt
txt
Copy
Edit
openai-agents
openai
requests
nest_asyncio
python-dotenv
🛑 .gitignore (Recommended)
bash
Copy
Edit
.venv/
venv/
.env
__pycache__/
📚 References
OpenRouter API Docs

OpenAI Agents SDK

Python dotenv

🧑‍💻 Author
Developed by Faraz Alam