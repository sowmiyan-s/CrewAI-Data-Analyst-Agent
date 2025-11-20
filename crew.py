
import logging
import sys
import os
from pathlib import Path
import pandas as pd
import webbrowser
from dotenv import load_dotenv

load_dotenv()

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("opentelemetry").setLevel(logging.ERROR)

if not os.getenv("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY environment variable is not set.")
    sys.exit(1)

try:
    from crewai import Crew
except ImportError as e:
    print(f"ERROR: {e}\nRun: pip install crewai")
    sys.exit(1)


def main():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 50)
    print("CrewAI Data Analyst")
    print("=" * 50)
    
    try:
        df = pd.read_csv("data/input.csv")
    except FileNotFoundError:
        print("Error: data/input.csv not found.")
        sys.exit(1)

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {', '.join(df.columns[:10])}...")


    from agents.cleaner import cleaner_agent
    from agents.validator import validator_agent
    from agents.relation import relation_agent
    from agents.code_gen import code_gen_agent
    from agents.insights import insights_agent
    from workflows.pipeline import (
        clean_task,
        validate_task,
        relation_task,
        code_task,
        insight_task,
    )
    
    crew = Crew(
        agents=[
            cleaner_agent,
            validator_agent,
            relation_agent,
            code_gen_agent,
            insights_agent,
        ],
        tasks=[
            clean_task,
            validate_task,
            relation_task,
            code_task,
            insight_task,
        ],
        verbose=True,
    )

    result = crew.kickoff()
    

    task_outputs = {}
    
   
    if hasattr(crew, 'tasks'):
        for i, task in enumerate(crew.tasks):
            if hasattr(task, 'output') and task.output:
                task_name = task.description.split()[0].lower()
                if hasattr(task.output, 'raw'):
                    task_outputs[task_name] = str(task.output.raw)
                else:
                    task_outputs[task_name] = str(task.output)
    
 
    if hasattr(result, 'raw'):
        final_output = str(result.raw)
    else:
        final_output = str(result)
    
 
    clean_output = task_outputs.get('clean', '')
    validate_output = task_outputs.get('validate', '')
    relation_output = task_outputs.get('identify', '')
    code_output = task_outputs.get('generate', '')
    insights_output = task_outputs.get('produce', final_output)
    

    code_path = output_dir / "op.py"
    if code_output and '```python' in code_output:
        import re
        code_match = re.search(r'```python\n(.*?)\n```', code_output, re.DOTALL)
        if code_match:
            code_path.write_text(code_match.group(1), encoding="utf-8")
    
    df_head = df.head(10).to_string(index=False)
    
    def prettify(section, content):
        if content and content.strip():
            
            content = str(content).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f"<h2>{section}</h2><pre><code>{content}</code></pre>"
        return f"<h2>{section}</h2><p><em>No data available</em></p>"
    
    html_blocks = []
    html_blocks.append(prettify("Dataset Preview (First 10 Rows)", df_head))
    html_blocks.append(prettify("1. Data Cleaning Steps", clean_output))
    html_blocks.append(prettify("2. Dataset Validation Result", validate_output))
    html_blocks.append(prettify("3. Identified Column Relations", relation_output))
    html_blocks.append(prettify("4. Generated Visualization Code", code_output))
    html_blocks.append(prettify("5. Data Insights", insights_output))
    
    final_blocks = "\n".join(html_blocks)

    html_report = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrewAI Data Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header {{
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .success {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.5em;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        pre {{
            background: #f8f9fa;
            padding: 20px;
            overflow-x: auto;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 15px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        code {{
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            color: #2c3e50;
            font-size: 0.9em;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .info-badge {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            margin: 5px;
        }}
        p em {{
            color: #95a5a6;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CrewAI Data Analysis Report</h1>
            <div>
                <span class="info-badge">Dataset: {len(df)} rows × {len(df.columns)} columns</span>
                <span class="info-badge">5 AI Agents</span>
                <span class="info-badge">Powered by Groq</span>
            </div>
        </div>
        <div class="success">
            ✅ Analysis pipeline completed successfully!
        </div>
        {final_blocks}
        <div class="footer">
            <p>Generated by CrewAI Multi-Agent System | LLM: Groq (llama-3.3-70b-versatile)</p>
        </div>
    </div>
</body>
</html>
"""
    
    report_file = Path("index.html")
    report_file.write_text(html_report, encoding="utf-8")
    print(f"\nReport saved: {report_file}")
    print("Analysis complete! Opening report in default browser...")
    webbrowser.open("index.html")


if __name__ == "__main__":
    main()
