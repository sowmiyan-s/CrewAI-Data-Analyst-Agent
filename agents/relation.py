from crewai import Agent, LLM

relation_agent = Agent(
    name="Analyst",
    role="Analyze dataset and identify key relationships",
    goal="Read data/input.csv and find numerical columns to visualize. Return JSON: [{'x':'col','y':'col','type':'scatter'}]",
    backstory="Data analysis expert. Fast and direct.",
    allow_delegation=False,
    llm=LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    ),
    verbose=True
)
