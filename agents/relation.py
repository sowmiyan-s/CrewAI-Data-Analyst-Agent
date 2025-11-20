from crewai import Agent, LLM
import os

relation_agent = Agent(
    name="Analyst",
    role="Analyze dataset and identify key relationships",
    goal="Read data/input.csv and find numerical columns to visualize. Return JSON: [{'x':'col','y':'col','type':'scatter'}]",
    backstory="Data analysis expert. Fast and direct.",
    allow_delegation=False,
    llm=LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    ),
    verbose=True
)
