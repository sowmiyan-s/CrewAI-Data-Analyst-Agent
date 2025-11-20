from crewai import Agent, LLM

code_gen_agent = Agent(
    name="Code Generator",
    role="Write visualization code",
    goal="Generate matplotlib code for the provided chart relations.",
    backstory="Python developer focused on matplotlib.",
    allow_delegation=False,
    llm=LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    ),
    verbose=True
)
