# openai_sdk_agent.py
import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

nest_asyncio.apply()
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-small-24b-instruct-2501:free"

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

async def main():
    agent = Agent(
        name="FarazTA",
        instructions="You only respond in English",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "What is your name and what is the weather in karachi on june 13 2004? ",
    )
    print("Agent SDK Response:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
