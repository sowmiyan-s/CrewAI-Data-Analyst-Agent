# CrewAI Data Analyst Agent

## Overview
A professional data analysis pipeline powered by LLM-driven agents using CrewAI and Groq. The application analyzes CSV datasets through multiple specialized agents that clean, validate, analyze relationships, generate visualization code, and provide insights.

## Current Status
- **Status**: Running successfully on Groq LLM
- **Server**: Running on port 5000
- **LLM Provider**: Groq (using llama-3.3-70b-versatile model)
- **Framework**: CrewAI with 5 specialized agents

## Recent Changes (November 20, 2025)
- Migrated from local Ollama to Groq cloud API
- Updated all agents to use Groq LLM provider
- Fixed server binding to 0.0.0.0:5000 for Replit environment
- Cleaned up unnecessary code and fixed LSP errors
- Added environment variable support for API key management
- Installed LiteLLM for CrewAI compatibility

## Project Architecture

### Agents (agents/)
1. **Data Cleaner** (`cleaner.py`) - Generates JSON cleaning instructions
2. **Dataset Validator** (`validator.py`) - Validates dataset usability
3. **Analyst** (`relation.py`) - Identifies visualization relationships
4. **Code Generator** (`code_gen.py`) - Writes matplotlib/seaborn code
5. **Insights Agent** (`insights.py`) - Generates data insights

### Workflows (workflows/)
- **pipeline.py** - Defines tasks connecting agents in sequence

### Entry Point
- **crew.py** - Main orchestration script that runs the pipeline and serves results

### Data
- **data/input.csv** - Input dataset (3069 rows, 17 columns)

### Outputs
- **outputs/op.py** - Generated Python visualization code
- **index.html** - Analysis report with results

## Configuration

### Environment Variables
- `GROQ_API_KEY` - API key for Groq LLM service (required)

### Dependencies
- crewai - Agent orchestration framework
- pandas - Data manipulation
- matplotlib & seaborn - Visualization
- litellm - LLM provider abstraction
- python-dotenv - Environment variable management

## How It Works
1. Loads CSV dataset from data/input.csv
2. Runs 5-agent pipeline: clean → validate → relation → code → insights
3. Generates HTML report with analysis results
4. Serves report on port 5000

## User Preferences
- Using Groq for LLM inference (cloud-based, fast)
- Error-free operation required
- Clean, production-ready code

## Deployment
- **Type**: VM (always running)
- **Command**: `python crew.py`
- **Port**: 5000 (webview)
