import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig, RunContextWrapper

# Load API key
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

    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        cl.run_sync(
            cl.Message(
                content=f"✈️ **Switching to `{agent.name}`...** Planning the next step!",
                author="System"
            ).send()
        )

    # TOOL: get_flights
    get_flights_agent = Agent(
        name="FlightToolAgent",
        instructions="Provides mock flight options to any destination.",
        model=model
    )

    # TOOL: suggest_hotels
    suggest_hotels_agent = Agent(
        name="HotelToolAgent",
        instructions="Suggests top-rated mock hotels in any destination.",
        model=model
    )

    # AGENT: BookingAgent (uses both tools)
    booking_agent = Agent(
        name="BookingAgent",
        instructions="""
        You assist users in booking travel by calling flight and hotel tools.
        Always use tools — never respond directly.
        """,
        tools=[
            get_flights_agent.as_tool("get_flights", "Provides flight options."),
            suggest_hotels_agent.as_tool("suggest_hotels", "Suggests hotels at destination.")
        ],
        model=model
    )

    # AGENT: DestinationAgent
    destination_agent = Agent(
        name="DestinationAgent",
        instructions="""
        You suggest travel destinations based on user's mood, preferences, or activities they enjoy.
        Include some rationale with each destination.
        """,
        model=model
    )

    # AGENT: ExploreAgent
    explore_agent = Agent(
        name="ExploreAgent",
        instructions="""
        Suggest things to do, places to eat, and local attractions at a given destination.
        You are like a local travel guide.
        """,
        model=model
    )

    # MAIN TRIAGE AGENT: TravelMasterAgent
    travel_master_agent = Agent(
        name="TravelMasterAgent",
        instructions="""
        You are the AI Travel Designer.
        - If user asks for destination ideas, hand off to DestinationAgent.
        - If user wants to book travel, hand off to BookingAgent.
        - If user wants to explore places, food, attractions, hand off to ExploreAgent.
        """,
        model=model,
        handoffs=[
            handoff(destination_agent, on_handoff=lambda ctx: on_handoff(destination_agent, ctx)),
            handoff(booking_agent, on_handoff=lambda ctx: on_handoff(booking_agent, ctx)),
            handoff(explore_agent, on_handoff=lambda ctx: on_handoff(explore_agent, ctx)),
        ]
    )

    cl.user_session.set("agent", travel_master_agent)
    cl.user_session.set("config", config)

    await cl.Message("🌍 Welcome to your AI Travel Designer!\nTell me where you want to go, or how you feel — and I’ll do the rest.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    msg = cl.Message(content="🧳 Planning your trip...")
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
