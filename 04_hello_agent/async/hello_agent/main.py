import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Gemini_API_KEY is not set.Please ensure it is defined in your .ev file.")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)
async def main():
    agent = Agent(
        name="Asistant",
        instructions="You are a helpful Assistant",
        model=model
    )
    result = await Runner.run(agent, "Tell me about recursion in child marrage in pakistan", run_config=config)
    print(result.final_output)
    ## output
    ##PS C:\Users\Lenovo\Desktop\python-giaic\learn_agentic_ai\04_hello_agent\async\hello_agent> uv run main.py
# Child marriage in Pakistan is a complex issue with deep roots in social, economic, and cultural factors. While "recursion" isn't the typical term used to describe it, the concept of a self-repeating cycle or pattern is highly relevant. Here's how the dynamics of child marriage can be seen as a recurring, cyclical problem:

# **How Child Marriage Becomes a Recurring Cycle:**

# *   **Poverty:** Impoverished families may see child marriage as a way to alleviate financial burdens. Marrying off a daughter reduces the number of mouths to feed and can bring in a bride price or dowry. Daughters of poor families are married off to slightly more affluent families, who consider women of lower status as assets and consider their reproduction and domestic labour as a way to overcome poverty. This perpetuates a cycle of poverty, as girls are denied education and economic opportunities. Their children are also more likely to live in poverty, and the cycle begins again.

# *   **Lack of Education:** Child marriage often prevents girls from completing their education. Without education, they have limited opportunities for economic independence and social mobility. They are then more likely to marry young themselves, perpetuating the cycle.  

# *   **Social Norms and Cultural Practices:** In some communities, child marriage is a deeply ingrained tradition. It may be seen as a way to protect girls from premarital sex, preserve family honor, or strengthen social bonds between families. These cultural norms are passed down through generations, making it difficult to break the cycle.

# *   **Gender Inequality:** Child marriage is a manifestation of gender inequality. Girls are often seen as less valuable than boys, and 
# their futures are determined by their families rather than themselves. This inequality is reinforced by child marriage, as girls are denied the same opportunities as boys.

# *   **Lack of Legal Enforcement:** While Pakistan has laws against child marriage, enforcement is often weak, especially in rural areas. This lack of accountability allows the practice to continue with impunity.

# *   **Health Consequences:** Child brides often face serious health risks, including complications during pregnancy and childbirth. These health problems can further limit their opportunities and perpetuate the cycle of poverty and inequality. The birth of children of child marriages also inherit the health problems of their mother, thereby continuing the cycle.

# **Breaking the Cycle:**

# To break the cycle of child marriage in Pakistan, a multi-faceted approach is needed:

# *   **Education:** Providing girls with access to quality education is crucial. Education empowers girls, increases their economic opportunities, and makes them less likely to marry young.
# *   **Economic Empowerment:** Programs that help families escape poverty can reduce the incentive to marry off daughters for financial reasons.
# *   **Legal Reform and Enforcement:** Strengthening laws against child marriage and ensuring that they are enforced effectively is essential.
# *   **Changing Social Norms:** Raising awareness about the harmful effects of child marriage and challenging traditional beliefs is necessary. This can be done through community outreach programs, media campaigns, and religious leaders.
# *   **Healthcare:** Providing access to reproductive healthcare and family planning services can help reduce the risks associated with early pregnancy and childbirth.

# In summary, the "recursive" or cyclical nature of child marriage in Pakistan means that it's a problem that reproduces itself across generations, driven by a complex interplay of factors. Addressing these factors in a comprehensive and sustained way is the only way to break the cycle and protect girls from this harmful practice.

if __name__ == "__main__":
    asyncio.run(main())