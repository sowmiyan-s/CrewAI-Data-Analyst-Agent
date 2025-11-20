#!/usr/bin/env python3
"""Simple CrewAI Data Analysis Pipeline"""
import logging
import sys
import webbrowser
from pathlib import Path
import pandas as pd

# Suppress logs
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("opentelemetry").setLevel(logging.ERROR)

try:
    from crewai import Crew
except ImportError as e:
    print(f"ERROR: {e}\nRun: pip install crewai")
    sys.exit(1)


def main():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 50)
    # Avoid Unicode error on Windows terminal
    try:
        print("🚀 CrewAI Data Analyst")
    except UnicodeEncodeError:
        print("CrewAI Data Analyst")
    print("=" * 50)
    
    # Remove excessive blanket try/except, only catch specific cases for user guidance or IO.
    try:
        df = pd.read_csv("data/input.csv")
    except FileNotFoundError:
        print("❌ Error: data/input.csv not found.")
        sys.exit(1)

    print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    print("\n🔍 Analyzing dataset...")
    print(f"   Columns: {', '.join(df.columns[:10])}...")

    print("\n▶️  Running full pipeline (clean -> validate -> relation -> code -> insights)\n")

    # Import all agents and tasks before crew instantiation
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
    # Build crew before use
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

    # Run pipeline
    output = crew.kickoff()

    # After running pipeline, attempt to parse out all intermediate agent outputs from the output result or by reading logs/files
    # Fallback: If you want true sequential control and context passing, you must run agents directly (not via Task pipeline) or
    # manually parse inter-results. For now, collect what you can:

    relation_output = None
    code_output = None
    try:
        # Crew's output is typically the last task; for richer outputs, enhance logging or parse from JSON
        if isinstance(output, dict) and "relation" in output:
            relation_output = output["relation"]
        elif isinstance(output, dict):
            # Try to find relation text in any key
            for k, v in output.items():
                if ("relation" in k or "viz" in k) and v:
                    relation_output = v
                    break
        elif isinstance(output, str):
            import re
            # Try to extract relation block as JSON (brute fallback)
            match = re.search(r'(\[\{.*?\}\])', output, re.DOTALL)
            if match:
                relation_output = match.group(1)
    except Exception:
        relation_output = None

    # If relation_output found, run code_gen agent to generate code for all relations, else fallback
    code_path = output_dir / "op.py"
    if relation_output:
        from agents.code_gen import code_gen_agent
        code_prompt = f"Generate matplotlib/seaborn code (save image to .png if plot) for each visualization in this list: {relation_output}"
        try:
            code_output = code_gen_agent.run(code_prompt)
            if code_output and isinstance(code_output, str):
                code_path.write_text(code_output, encoding="utf-8")
                print("✓ op.py saved!")
        except Exception as e:
            print(f"❌ Failed to run code_gen agent or save op.py: {e}")
    else:
        try:
            if code_path.exists() and code_path.stat().st_size > 0:
                code_output = code_path.read_text(encoding="utf-8")
        except Exception:
            code_output = ""

    # Execute op.py and embed output as before...
    op_stdout, op_img = None, None
    if code_path.exists() and code_path.stat().st_size > 0:
        import subprocess, io, contextlib
        from glob import glob
        img_files_before = set(glob(str(output_dir / "*.png")))
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                try:
                    proc = subprocess.run([sys.executable, str(code_path)],
                                         capture_output=True, text=True, cwd=str(output_dir), timeout=30)
                    op_stdout = proc.stdout + ("\n[stderr]\n" + proc.stderr if proc.stderr else "")
                except subprocess.TimeoutExpired:
                    op_stdout = "❌ op.py execution timed out."
                except Exception as e:
                    op_stdout = f"❌ Error running op.py: {e}"
        finally:
            img_files_after = set(glob(str(output_dir / "*.png")))
            new_imgs = img_files_after - img_files_before
            op_img = next(iter(new_imgs), None) if new_imgs else None
    else:
        op_stdout = "No op.py or code generated."
        op_img = None

    # Continue assembling your html blocks etc. as before, using whatever outputs could be parsed.
    df_head = None
    try:
        df_head = df.head().to_markdown(index=False)
    except Exception:
        df_head = df.head().to_string(index=False)
    html_blocks = []
    def prettify(presection, content):
        return f"<h2>{presection}</h2><pre><code>{content}</code></pre>" if content else f"<h2>{presection}</h2><em>No data.</em>"
    html_blocks.append(prettify("First 5 Rows of Dataset", df_head))
    html_blocks.append(prettify("Cleaning Steps", output.get('clean')))
    html_blocks.append(prettify("Validation Result", output.get('validate')))
    html_blocks.append(prettify("Identified Column Relations", relation_output))
    html_blocks.append(prettify("Generated Python Code (op.py)", code_output))
    html_blocks.append(prettify("Generated Insights", output.get('insight')))
    if op_img:
        html_blocks.append(f'<h2>op.py Generated Image</h2><img src="outputs/{Path(op_img).name}" alt="Chart" style="max-width:100%">')
    if op_stdout:
        html_blocks.append(prettify("op.py Console Output", op_stdout))
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
        <h1>✅ CrewAI Analysis Complete</h1>
        <div class="success">Pipeline executed successfully on {len(df)} rows</div>
        {final_blocks}
        <h2>Dataset Info</h2>
        <pre><code>{df.info()}</code></pre>
    </div>
</body>
</html>
"""
    
    # Save HTML with UTF-8 encoding
    report_file = Path("index.html")
    report_file.write_text(html_report, encoding="utf-8")
    print(f"OK Report saved: {report_file}")
    
    # Start a simple local HTTP server to serve the report and keep process alive
    print("\n🌐 Serving report at http://localhost:8000/index.html (press Ctrl+C to stop)")

    try:
        from http.server import SimpleHTTPRequestHandler
        from socketserver import ThreadingTCPServer
        import threading

        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

        server = ThreadingTCPServer(("", 8000), QuietHandler)

        def serve():
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass

        t = threading.Thread(target=serve, daemon=True)
        t.start()

        webbrowser.open("http://localhost:8000/index.html")

        # Block until user interrupts
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            server.shutdown()
            server.server_close()
            print("Stopped.")

    except Exception as e:
        print(f"   ⚠️  Could not start local server: {e}")
        print("   The report is saved at:", report_file.absolute())
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

