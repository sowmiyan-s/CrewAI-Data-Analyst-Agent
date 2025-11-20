from crewai import Agent, LLM

cleaner_agent = Agent(
    name="Data Cleaner",
    role="Clean dataset",
    backstory="A no-nonsense data mechanic who hates messy CSVs. You grew up debugging trash datasets and built a rep for turning corrupt data into clean, analysis-ready gold.",
    goal="Generate JSON instructions for cleaning dataframe without modifying code.",
    llm=LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    ),
    verbose=True
)
