# 🧠 Health & Wellness Planner Agent

### 👤 Author:Faraz Alam

### 🆔 Roll No:6464

### 📚 Project Type: Assignment

### 💼 Platform: Terminal-based AI Agent using Gemini API

---

## 📌 Project Overview

The **Health & Wellness Planner Agent** is a terminal-based AI project designed to assist users in achieving their fitness and diet goals. It leverages the **Google Gemini API** using a modular architecture inspired by the **OpenAI Agents SDK**.

This agent interacts with the user to:

- Understand their health goals
- Recommend personalized meal and workout plans
- Schedule progress check-ins
- Track progress over time
- Provide expert handoffs (e.g., nutrition or injury support) when needed

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/health_wellness_agent.git
cd health_wellness_agent

2. Install Dependencies
pip install -r requirements.txt
Make sure Python 3.11 or above is installed.

3. Setup Environment Variable
Create a .env file in the project root with your Gemini API key:

GEMINI_API_KEY=your_google_gemini_api_key_here
4. Run the Application
python main.py
You can now interact with the AI in your terminal.

📁 Project Folder Structure
health_wellness_agent/
├── main.py                           # Entry point of the app
├── agent.py                          # Main AI agent configuration
├── context.py                        # Session or user context handling
├── guardrails.py                     # Optional guardrails logic
├── hooks.py                          # Lifecycle hooks for the agent
├── .env                              # Contains GEMINI_API_KEY (not uploaded to GitHub)
├── .gitignore                        # Ignore .env and other unnecessary files
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── agents/                           # Expert agents for handoffs
│   ├── escalation_agent.py
│   ├── nutrition_expert_agent.py
│   └── injury_support_agent.py
├── tools/                            # Agent tool implementations
│   ├── goal_analyzer.py
│   ├── meal_planner.py
│   ├── workout_recommender.py
│   ├── scheduler.py
│   └── tracker.py
└── utils/
    └── streaming.py                 # For real-time output (optional)

🛠 Technologies Used

Python 3.11+

Google Gemini API (OpenAI-compatible interface)

OpenAI Agents SDK (structure inspired)

Modular file system (tools, agents, hooks, utils)

Terminal-based interface (CLI)

🔐 Environment Variables
Variable Name	Description
GEMINI_API_KEY	Your Google Gemini API Key (secret)

⚠️ Never upload your .env file to GitHub. It's already included in .gitignore.
```
