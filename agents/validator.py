from crewai import Agent, LLM
import os

validator_agent = Agent(
    name="Dataset Validator",
    role="Validate dataset usability",
    goal="Return JSON {decision: YES/NO, reason: text}. If NO, pipeline stops.",
    backstory="A strict dataset gatekeeper. You don't sugarcoat garbage data. If a dataset sucks, you shut the whole pipeline down without hesitation.",
    llm=LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    ),
    verbose=True
)
