from crewai import Agent, LLM
import os

code_gen_agent = Agent(
    name="Code Generator",
    role="Write visualization code",
    goal="Generate matplotlib code for the provided chart relations.",
    backstory="Python developer focused on matplotlib.",
    allow_delegation=False,
    llm=LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    ),
    verbose=True
)
