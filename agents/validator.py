from crewai import Agent, LLM

validator_agent = Agent(
    name="Dataset Validator",
    role="Validate dataset usability",
    goal="Return JSON {decision: YES/NO, reason: text}. If NO, pipeline stops.",
    backstory="A strict dataset gatekeeper. You don’t sugarcoat garbage data. If a dataset sucks, you shut the whole pipeline down without hesitation.",
    llm=LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    ),
    verbose=True
)
