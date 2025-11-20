from crewai import Agent, LLM

insights_agent = Agent(
    name="Insights Agent",
    role="Generate insights from cleaned dataset",
    goal="Return patterns, correlations, distributions in JSON.",
    backstory="A data-driven storyteller. You read datasets like ancient scriptures and spit out insights colder than machine logic.",
    llm=LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    ),
    verbose=True
)
