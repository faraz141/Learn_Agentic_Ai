import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig, RunContextWrapper

# Load API keys
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please define it in your .env file.")

@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

    # Handoff display
    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        cl.run_sync(
            cl.Message(
                content=f"🎭 **Switching to `{agent.name}`...**",
                author="System"
            ).send()
        )

    # TOOL: Dice Roller
    dice_roller = Agent(
        name="DiceRollerAgent",
        instructions="Rolls a 6-sided dice. Always returns a number between 1-6.",
        model=model
    )

    # TOOL: Event Generator
    event_generator = Agent(
        name="EventGeneratorAgent",
        instructions="Creates a fantasy event for the player to experience based on the current situation.",
        model=model
    )

    # AGENT: Monster (Combat)
    monster_agent = Agent(
        name="MonsterAgent",
        instructions="Handles battles and monster encounters. Describe the enemy and combat using dice outcomes.",
        tools=[
            dice_roller.as_tool("roll_dice", "Rolls a 6-sided die to determine damage or outcomes.")
        ],
        model=model
    )

    # AGENT: Inventory (Items and Rewards)
    item_agent = Agent(
        name="ItemAgent",
        instructions="Manages the player's inventory, rewards, and special items.",
        model=model
    )

    # AGENT: Narrator
    narrator_agent = Agent(
        name="NarratorAgent",
        instructions="""
        Tells the story. Guides the player based on their choices.
        Always use the event generator to create plot points.
        Never generate events yourself — use the tool.
        """,
        tools=[
            event_generator.as_tool("generate_event", "Generates a fantasy story event.")
        ],
        model=model
    )

    # MAIN TRIAGE AGENT: Game Master
    game_master_agent = Agent(
        name="GameMasterAgent",
        instructions="""
        You are the Game Master. Based on the player input:
        - If it's a story decision, hand off to NarratorAgent.
        - If they encounter enemies or say 'fight', hand off to MonsterAgent.
        - If they find loot, ask about gear, or rewards, hand off to ItemAgent.
        """,
        model=model,
        handoffs=[
            handoff(narrator_agent, on_handoff=lambda ctx: on_handoff(narrator_agent, ctx)),
            handoff(monster_agent, on_handoff=lambda ctx: on_handoff(monster_agent, ctx)),
            handoff(item_agent, on_handoff=lambda ctx: on_handoff(item_agent, ctx)),
        ]
    )

    cl.user_session.set("agent", game_master_agent)
    cl.user_session.set("config", config)

    await cl.Message("🧙 Welcome, brave adventurer!\n\nYour story begins now. What will you do?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    msg = cl.Message(content="🎲 Rolling fate...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_sync(agent, history, run_config=config)
        msg.content = result.final_output
        await msg.update()

        history.append({"role": "assistant", "content": result.final_output})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()
