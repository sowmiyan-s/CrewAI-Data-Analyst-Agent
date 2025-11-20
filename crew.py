#!/usr/bin/env python3
"""Simple CrewAI Data Analysis Pipeline"""
import logging
import sys
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("opentelemetry").setLevel(logging.ERROR)

if not os.getenv("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY environment variable is not set.")
    print("Please set your Groq API key in the Replit Secrets tab.")
    print("Get your API key from: https://console.groq.com/keys")
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
    print("\nRunning full pipeline (clean -> validate -> relation -> code -> insights)\n")

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

    output = crew.kickoff()

    output_dict = {}
    if isinstance(output, dict):
        output_dict = output
    elif hasattr(output, '__dict__'):
        output_dict = output.__dict__
    
    code_path = output_dir / "op.py"
    code_output = ""
    if code_path.exists() and code_path.stat().st_size > 0:
        try:
            code_output = code_path.read_text(encoding="utf-8")
        except Exception:
            code_output = ""

    df_head = df.head().to_string(index=False)
    
    def prettify(section, content):
        if content:
            return f"<h2>{section}</h2><pre><code>{content}</code></pre>"
        return f"<h2>{section}</h2><em>No data.</em>"
    
    html_blocks = []
    html_blocks.append(prettify("First 5 Rows of Dataset", df_head))
    html_blocks.append(prettify("Cleaning Steps", output_dict.get('clean', '')))
    html_blocks.append(prettify("Validation Result", output_dict.get('validate', '')))
    html_blocks.append(prettify("Identified Column Relations", output_dict.get('relation', '')))
    html_blocks.append(prettify("Generated Python Code (op.py)", code_output))
    html_blocks.append(prettify("Generated Insights", output_dict.get('insight', '')))
    
    final_blocks = "\n".join(html_blocks)

    html_report = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrewAI Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: #f5f5f5;
        }}
        .container {{
            max-width: 900px; margin: 0 auto; background: white;
            border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .success {{ background: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 10px 0; }}
        pre {{ background: #f8f9fa; padding: 15px; overflow-x: auto; border-radius: 4px; }}
        code {{ font-family: 'Courier New', monospace; color: #555; }}
        img {{ display: block; margin: 1em auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>CrewAI Analysis Complete</h1>
        <div class="success">Pipeline executed successfully on {len(df)} rows</div>
        {final_blocks}
    </div>
</body>
</html>
"""
    
    report_file = Path("index.html")
    report_file.write_text(html_report, encoding="utf-8")
    print(f"\nReport saved: {report_file}")
    print("Analysis complete! View the report at http://0.0.0.0:5000")
    
    from http.server import SimpleHTTPRequestHandler
    from socketserver import ThreadingTCPServer

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    server = ThreadingTCPServer(("0.0.0.0", 5000), QuietHandler)
    
    print("\nServing report on port 5000...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
