import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff, Tool
from agents.run import RunConfig, RunContextWrapper

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")




@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        cl.run_sync(
            cl.Message(
                content=f"🔄 **Handing off to {agent.name}...**\n\nTransferring you to a specialized assistant.",
                author="System"
            ).send()
        )

    # Define all agents
    get_career_roadmap_agent = Agent(
        name="career_roadmap_agent",
        instructions="""
        You provide a detailed step-by-step skill roadmap for the given career field.
        The user will specify a field like 'Web Development' or 'Data Science', and you must return a clear learning plan.
        Example format:
        1. Step One
        2. Step Two
        ...
        """,
        model=model
    )
    job_agent = Agent(
        name="JobAgent",
        instructions="You are JobAgent, a helpful assistant that provides information about real-world job roles: responsibilities, salary, qualifications, and how to enter the field.",
        model=model
    )

    skill_agent = Agent(
        name="skill_agent",
        instructions="""
        You help users build skills for a specific career.
        Use the tool 'get_career_roadmap' to fetch the step-by-step roadmap.
        Never answer directly, always call the tool.
        """,
        tools=[
            get_career_roadmap_agent.as_tool(
                tool_name="get_career_roadmap",
                tool_description="Provides a step-by-step skill roadmap for a specific career field like 'Web Development'"
            )
        ],
        model=model
    )

    career_agent = Agent(
        name="CareerAgent",
        instructions="You are CareerAgent. Based on the user's interests, strengths, or background, suggest career fields and explain why each might be a good fit.",
        model=model
    )

    triage_agent = Agent(
        name="TriageAgent",
        instructions="""
        You are the Career Mentor Agent. Based on the user's message:
        - If they ask about career options → handoff to CareerAgent
        - If they want to build skills → handoff to SkillAgent
        - If they ask about job roles → handoff to JobAgent
        """,
        model=model,
        handoffs=[
            handoff(career_agent, on_handoff=lambda ctx: on_handoff(career_agent, ctx)),
            handoff(skill_agent, on_handoff=lambda ctx: on_handoff(skill_agent, ctx)),
            handoff(job_agent, on_handoff=lambda ctx: on_handoff(job_agent, ctx)),
        ]
    )

    # Store in session
    cl.user_session.set("agent", triage_agent)
    cl.user_session.set("config", config)

    await cl.Message(content="🎓 Welcome to the Career Mentor Agent!\n\nHow can I help you with your career journey today?").send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_sync(agent, history, run_config=config)
        response_content = result.final_output

        msg.content = response_content
        await msg.update()

        history.append({"role": "developer", "content": response_content})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()
