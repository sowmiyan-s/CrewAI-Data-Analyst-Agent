from crewai import Agent, LLM
import os

cleaner_agent = Agent(
    name="Data Cleaner",
    role="Clean dataset",
    backstory="A no-nonsense data mechanic who hates messy CSVs. You grew up debugging trash datasets and built a rep for turning corrupt data into clean, analysis-ready gold.",
    goal="Generate JSON instructions for cleaning dataframe without modifying code.",
    llm=LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    ),
    verbose=True
)
