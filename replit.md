# CrewAI Data Analyst Agent

## Overview
A professional data analysis pipeline powered by LLM-driven agents using CrewAI and Groq. The application analyzes CSV datasets through multiple specialized agents that clean, validate, analyze relationships, generate visualization code, and provide insights.

## Current Status
- **Status**: ✅ Running successfully
- **Server**: Running on port 5000
- **LLM Provider**: Groq (configurable via `config/llm_config.py`)
- **Framework**: CrewAI with 5 specialized agents
- **HTML Report**: Properly displaying all agent responses

## Recent Changes (November 20, 2025)
- ✅ Created centralized LLM configuration system (`config/llm_config.py`)
- ✅ Updated all agents to use centralized config
- ✅ Fixed HTML report to properly display all LLM responses from agents
- ✅ Added support for multiple LLM providers (Groq, OpenAI, Anthropic, Ollama)
- ✅ Added comprehensive documentation for LLM configuration
- Migrated from local Ollama to Groq cloud API
- Fixed server binding to 0.0.0.0:5000 for Replit environment
- Cleaned up unnecessary code and fixed LSP errors
- Added environment variable support for API key management

## Project Architecture

### Configuration (config/)
- **llm_config.py** - Centralized LLM provider configuration
  - Supports switching between Groq, OpenAI, Anthropic, Ollama
  - Controlled via `LLM_PROVIDER` environment variable
  - Validates credentials before initializing agents
  - See `config/README.md` for detailed usage instructions

### Agents (agents/)
All agents now use centralized LLM config via `from config.llm_config import get_llm_params`

1. **Data Cleaner** (`cleaner.py`) - Generates JSON cleaning instructions
2. **Dataset Validator** (`validator.py`) - Validates dataset usability
3. **Analyst** (`relation.py`) - Identifies visualization relationships
4. **Code Generator** (`code_gen.py`) - Writes matplotlib/seaborn code
5. **Insights Agent** (`insights.py`) - Generates data insights

### Workflows (workflows/)
- **pipeline.py** - Defines tasks connecting agents in sequence

### Entry Point
- **crew.py** - Main orchestration script that:
  - Runs the 5-agent pipeline
  - Extracts task outputs from CrewAI
  - Generates HTML report with all agent responses
  - Serves report on port 5000

### Data
- **data/input.csv** - Input dataset (3069 rows, 17 columns)

### Outputs
- **outputs/op.py** - Generated Python visualization code
- **index.html** - Analysis report with all agent responses displayed

## Configuration

### Environment Variables
- `LLM_PROVIDER` - Choose LLM provider: groq (default), openai, anthropic, ollama
- `GROQ_API_KEY` - API key for Groq (required if using Groq)
- `OPENAI_API_KEY` - API key for OpenAI (required if using OpenAI)
- `ANTHROPIC_API_KEY` - API key for Anthropic (required if using Anthropic)
- `OLLAMA_BASE_URL` - Base URL for Ollama (default: http://localhost:11434)

See `.env.example` for full configuration template.

### Switching LLM Providers
1. Set `LLM_PROVIDER` environment variable to desired provider
2. Add corresponding API key to Replit Secrets
3. Restart the workflow

**No code changes needed!** All agents automatically use the centralized config.

### Dependencies
- crewai - Agent orchestration framework
- pandas - Data manipulation
- matplotlib & seaborn - Visualization
- litellm - LLM provider abstraction
- python-dotenv - Environment variable management

## How It Works
1. Loads CSV dataset from data/input.csv
2. Runs 5-agent pipeline: clean → validate → relation → code → insights
3. Extracts outputs from each task
4. Generates HTML report with all agent responses
5. Serves report on port 5000

## User Preferences
- Using Groq for LLM inference (cloud-based, fast)
- Centralized LLM configuration for easy provider switching
- Error-free operation required
- Clean, production-ready code
- All agent responses must be visible in HTML report

## Deployment
- **Type**: VM (always running)
- **Command**: `python crew.py`
- **Port**: 5000 (webview)

## Documentation
- **config/README.md** - Comprehensive LLM configuration guide
- **.env.example** - Environment variable template with examples
