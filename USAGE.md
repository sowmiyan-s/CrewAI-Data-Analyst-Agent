# 🚀 Quick Start Guide

## Simple & Clean Workflow

The pipeline is now **streamlined and simple**:

```
crew.py → Load CSV → Analyze Dataset → Open Browser → Done
```

## Prerequisites

1. **Python 3.8+**
2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Ollama (Optional)** - If you want LLM analysis:
   - Download from https://ollama.ai
   - Run: `ollama pull llama3`
   - Keep running in background

## Run Analysis

```powershell
python crew.py
```

**That's it!** The script will:
- ✅ Load `data/input.csv`
- ✅ Run agent analysis
- ✅ Generate HTML report
- ✅ Open browser automatically
- ✅ Save results to `index.html`

## Project Structure

```
crew.py                 # Main entry point
data/input.csv          # Your dataset
index.html              # Generated report
outputs/                # Analysis results
agents/
  └── relation.py       # Analysis agent
workflows/
  └── pipeline.py       # Task definitions
```

## Workflow

1. **Analyze** → Agent scans CSV columns
2. **Identify** → Finds relationships for visualization
3. **Report** → HTML output in browser

No complexity. No mess. Just data analysis.

## Troubleshooting

**"ModuleNotFoundError"**
```powershell
pip install crewai pandas
```

**"Connection refused"**
- Make sure Ollama is running (if using LLM)
- Or data analysis will work without it

**"UnicodeEncodeError"**
- Already fixed! Uses UTF-8 encoding

## Output

- `index.html` - Beautiful analysis report
- Console - Live pipeline execution
- Browser - Auto-opens with results

That's all you need! 🎉
