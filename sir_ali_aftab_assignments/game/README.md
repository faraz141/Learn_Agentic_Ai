# 🧙 Fantasy Adventure Game - AI Agent System

A text-based fantasy RPG powered by AI agents, tools, and dynamic handoffs!

---

## 🎮 What It Does

This interactive system allows users to play a fantasy adventure game driven by multiple AI agents. Each agent specializes in part of the game: narration, combat, or inventory. The Game Master agent routes player actions to the appropriate specialist.

---

## ⚙️ Features

- **🗺️ NarratorAgent**: Guides story progression and uses `generate_event` to drive the plot.
- **🧟 MonsterAgent**: Handles battles and enemy encounters, using `roll_dice` to determine outcomes.
- **🎁 ItemAgent**: Manages rewards, inventory, and special items.
- **🎲 Tools**:
  - `generate_event`: Creates fantasy scenarios.
  - `roll_dice`: Simulates dice-based combat or outcomes.
- **🎭 GameMasterAgent**: The main controller that hands off between agents based on user input.

---

## 🧩 Agent & Tool Flow

````mermaid
flowchart TD
    PlayerInput --> GameMasterAgent
    GameMasterAgent --> NarratorAgent
    GameMasterAgent --> MonsterAgent
    GameMasterAgent --> ItemAgent
    NarratorAgent --> EventTool[generate_event]
    MonsterAgent --> DiceTool[roll_dice]

📁 Project Structure

```fantasy-adventure/
├── main.py              # Main app logic
├── .env                 # GEMINI_API_KEY config
├── pyproject.toml       # Dependencies
├── README.md            # You're reading it!

````

🚀 Getting Started
Install dependencies:
uv venv
uv pip install chainlit openai-agents python-dotenv
Add your .env file:

GEMINI_API_KEY=your_api_key_here
Run the game:
chainlit run main.py
