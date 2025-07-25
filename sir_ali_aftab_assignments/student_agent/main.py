import os
import asyncio
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Set up the Gemini API client and model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define your custom agent
agent = Agent(
    name="StudentAssistant",
    instructions="""
    You are a Smart Student Assistant. You can:
    - Answer academic questions clearly.
    - Give effective study tips.
    - Summarize short paragraphs of text.
    Keep your answers short, helpful, and student-friendly.
    """,
    model=model
)

# Chainlit message handler
@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(agent, message.content, run_config=config)
    await cl.Message(content=result.final_output).send()
