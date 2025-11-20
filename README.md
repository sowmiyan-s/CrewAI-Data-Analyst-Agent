<!-- Enhanced README: hero, badges, tech icons, screenshots -->

<p align="center">
	<img src="assets/hero.svg" alt="CrewAI Hero" width="900" />
</p>

# CrewAI — Data Analyst Agent

<p align="center">
	<img src="assets/stars.svg" alt="5-star" height="28" />
	&nbsp;&nbsp;
	<img src="assets/badge_crewai.svg" alt="crewai" height="28" />
	<img src="assets/badge_pandas.svg" alt="pandas" height="28" />
	<img src="assets/badge_matplotlib.svg" alt="matplotlib" height="28" />
	<img src="assets/badge_seaborn.svg" alt="seaborn" height="28" />
	<img src="assets/badge_ollama.svg" alt="ollama" height="28" />
</p>

> A professional, modular data-analyst pipeline powered by LLM-driven agents. Feed it a CSV and it will propose cleaning, validate data, suggest visual relationships, generate runnable matplotlib/seaborn code, and produce written insights.

## Quick Links

- Run: `python crew.py`
- Outputs: `outputs/op.py`, `index.html`
- Agents: `agents/` — each agent defines its LLM model and endpoint.

## Quick Start

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start your LLM backend (example: Ollama) and ensure it listens at the address used in `agents/*.py` (default `http://localhost:11434`).

```powershell
ollama serve
```

3. Run the pipeline:

```powershell
python crew.py
```

## What you'll get

- `outputs/op.py` — collected Python snippets extracted from agent outputs (if any).
- `index.html` — a human-friendly summary (raw JSON + highlighted, copyable code blocks).

## Tech & Integrations

This project is lightweight and focused on composability. Key technologies:

- `crewai` — orchestration and agent primitives
- `pandas` — tabular data handling
- `matplotlib` / `seaborn` — visualization code generation
- `Ollama` (or compatible LLM HTTP API) — LLM backend used by the agents

### Tech Icons

<p>
	<img src="assets/badge_pandas.svg" alt="pandas" style="margin-right:8px" />
	<img src="assets/badge_matplotlib.svg" alt="matplotlib" style="margin-right:8px" />
	<img src="assets/badge_seaborn.svg" alt="seaborn" style="margin-right:8px" />
	<img src="assets/badge_ollama.svg" alt="ollama" style="margin-right:8px" />
</p>

## Views / Screenshots

- The repository includes a responsive `index.html` (rendered after a run) which highlights raw JSON and generated Python snippets. Open it locally to inspect outputs and copy code blocks quickly.

## Project Structure

```
├── agents/               # Agent definitions (cleaner, validator, relation, code_gen, insights)
├── tools/                # Helper utilities (e.g. dataframe_ops.apply_cleaning)
├── data/                 # Example input CSVs
├── outputs/              # Generated code and artifacts (op.py, index.html)
├── assets/               # Images and SVGs used by README/UI
├── crew.py               # Entry point that wires agents and kicks off the pipeline
├── workflows/pipeline.py # Task definitions connecting agents to tasks
```

## Customization

- Edit agents in `agents/*.py` to change model, `base_url`, or prompt backstories.
- Add or change `Task` definitions in `workflows/pipeline.py` to adjust behavior or add steps.

## Next steps I can help with

- Embed extracted code directly into `index.html` from `crew.py` after a run.
- Add a sample demo script that applies `tools/dataframe_ops.apply_cleaning` to `data/input.csv` and writes example outputs.
- Create a `docker-compose` or local setup script for running Ollama and the pipeline together.

---

If you want a different visual style (dark/light), more badges, or real screenshot images instead of SVG placeholders, tell me which style and I will add them.

