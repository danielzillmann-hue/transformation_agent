import os
import json
import asyncio
import uuid
from typing import List, Optional
from queue import Queue
from threading import Thread

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, StreamingResponse
from google.cloud import storage

from src.service import run_pipeline

app = FastAPI(title="Sybase to BigQuery Agentic Migration API")

BASE_OUTPUT_ROOT = "runs"


def _list_gcs_buckets(project_id: str = "dan-sandpit") -> list[str]:
    """Return all GCS bucket names in the given project.

    For the POC we list all buckets in dan-sandpit so users can
    select both the source and archive buckets from dropdowns.
    """
    try:
        client = storage.Client(project=project_id)
        return sorted([b.name for b in client.list_buckets()])
    except Exception:
        # Fail soft: if listing fails, return an empty list and the
        # HTML will fall back to a disabled select.
        return []


@app.get("/", response_class=HTMLResponse)
async def index():
    project_id = os.getenv("GCP_PROJECT_ID", "dan-sandpit")
    buckets = _list_gcs_buckets(project_id)

    def _options(selected: Optional[str] = None) -> str:
        if not buckets:
            return "<option value=\"\" disabled>No buckets found</option>"
        opts = []
        for name in buckets:
            sel = " selected" if selected and name == selected else ""
            opts.append(f"<option value=\"{name}\"{sel}>{name}</option>")
        return "".join(opts)

    source_bucket_default = "crownpoc" if "crownpoc" in buckets else (buckets[0] if buckets else "")
    archive_bucket_placeholder = "e.g. crownpoc-results"

    return f"""<!doctype html>
    <html>
    <head>
      <title>Sybase to BigQuery Agentic Migration</title>
      <style>
        :root {{
          color-scheme: light dark;
          --bg: #0f172a;
          --bg-card: #020617;
          --border-subtle: rgba(148, 163, 184, 0.4);
          --accent: #22c55e;
          --accent-soft: rgba(34, 197, 94, 0.16);
          --text: #e5e7eb;
          --muted: #9ca3af;
        }}
        body {{
          margin: 0;
          min-height: 100vh;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: radial-gradient(circle at top left, #1e293b 0, #020617 40%, #020617 100%);
          color: var(--text);
          display: flex;
          align-items: stretch;
          justify-content: center;
        }}
        .shell {{
          max-width: 1100px;
          width: 100%;
          padding: 2.5rem 1.5rem 3rem;
        }}
        .header {{
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-bottom: 2rem;
        }}
        .title-row {{
          display: flex;
          align-items: center;
          gap: 0.6rem;
        }}
        .pill {{
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          padding: 0.18rem 0.55rem;
          border-radius: 999px;
          border: 1px solid var(--border-subtle);
          color: var(--muted);
        }}
        h1 {{
          font-size: 1.6rem;
          font-weight: 600;
          margin: 0;
        }}
        .subtitle {{
          font-size: 0.95rem;
          color: var(--muted);
          max-width: 640px;
        }}
        .grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
          gap: 1.25rem;
        }}
        .card {{
          background: radial-gradient(circle at top left, rgba(34,197,94,0.05), #020617 55%);
          border-radius: 0.9rem;
          border: 1px solid rgba(148,163,184,0.35);
          padding: 1.4rem 1.4rem 1.5rem;
          box-shadow: 0 18px 45px rgba(15,23,42,0.85);
        }}
        .card h2 {{
          font-size: 1.05rem;
          margin: 0 0 0.4rem;
        }}
        .card p {{
          margin: 0 0 0.9rem;
          font-size: 0.9rem;
          color: var(--muted);
        }}
        form {{
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-top: 0.5rem;
        }}
        label {{
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          font-size: 0.8rem;
          color: var(--muted);
        }}
        input[type="text"], input[type="file"] {{
          border-radius: 0.45rem;
          border: 1px solid rgba(148,163,184,0.55);
          padding: 0.45rem 0.6rem;
          background: rgba(15,23,42,0.85);
          color: var(--text);
          font-size: 0.85rem;
        }}
        input[type="file"] {{
          padding: 0.35rem 0.6rem;
        }}
        input[type="checkbox"] {{
          accent-color: var(--accent);
        }}
        .inline-option {{
          display: flex;
          align-items: center;
          gap: 0.45rem;
          font-size: 0.8rem;
          color: var(--muted);
        }}
        button[type="submit"] {{
          margin-top: 0.6rem;
          align-self: flex-start;
          border-radius: 999px;
          border: 0;
          padding: 0.5rem 1.1rem;
          font-size: 0.85rem;
          font-weight: 500;
          background: linear-gradient(135deg, var(--accent), #4ade80);
          color: #022c22;
          cursor: pointer;
          box-shadow: 0 12px 30px rgba(34,197,94,0.5);
        }}
        button[type="submit"]:hover {{
          filter: brightness(1.05);
        }}
        .footer-note {{
          margin-top: 1.6rem;
          font-size: 0.8rem;
          color: var(--muted);
        }}
        code {{
          background: rgba(15,23,42,0.9);
          padding: 0.1rem 0.35rem;
          border-radius: 0.25rem;
        }}
      </style>
    </head>
    <body>
      <div class="shell">
        <header class="header">
          <div class="title-row">
            <div class="pill">Agentic migration</div>
            <h1>Sybase → BigQuery transformation agent</h1>
          </div>
          <p class="subtitle">
            Orchestrate schema analysis, business-domain mapping, Dataform generation,
            and validation tests for Sybase + Informatica workloads.
          </p>
        </header>

        <div class="grid">
          <section class="card">
            <h2>Run using GCS bucket</h2>
            <p>Point the agent at a Sybase / Informatica export in a Cloud Storage bucket.</p>
            <form action="/runs/gcs" method="post">
              <label>GCS Bucket
                <select name="bucket" required>
                  {_options(source_bucket_default)}
                </select>
              </label>
              <label>GCP Project ID
                <input type="text" name="project" value="{project_id}" />
              </label>
              <label>Archive results to GCS bucket (optional)
                <select name="archive_bucket">
                  <option value="">-- None --</option>
                  {_options()}
                </select>
              </label>
              <div class="inline-option">
                <input type="checkbox" name="skip_analysis" value="true" />
                <span>Skip analysis (reuse existing <code>analysis_results.json</code> for this run)</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="categorize" value="true" checked />
                <span>Run business-domain categorisation</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="translate" value="true" checked />
                <span>Generate BigQuery / Dataform project</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="validate" value="true" checked />
                <span>Create validation test definitions</span>
              </div>
              <button type="submit">Start GCS run</button>
            </form>
          </section>

          <section class="card">
            <h2>Run using local file upload</h2>
            <p>Upload Sybase DDL / stored procedures and Informatica XML exports directly.</p>
            <form action="/runs/local" method="post" enctype="multipart/form-data">
              <label>Files
                <input type="file" name="files" multiple required />
              </label>
              <label>GCP Project ID
                <input type="text" name="project" value="dan-sandpit" />
              </label>
              <div class="inline-option">
                <input type="checkbox" name="skip_analysis" value="true" />
                <span>Skip analysis (not usually needed for uploads)</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="categorize" value="true" checked />
                <span>Run business-domain categorisation</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="translate" value="true" checked />
                <span>Generate BigQuery / Dataform project</span>
              </div>
              <div class="inline-option">
                <input type="checkbox" name="validate" value="true" checked />
                <span>Create validation test definitions</span>
              </div>
              <button type="submit">Start local run</button>
            </form>
          </section>
        </div>

        <p class="footer-note">
          After a run completes, you'll see a run ID and a link to a summary page with
          download links for reports, dependency graph, validations, and the Dataform project.
        </p>
      </div>
    </body>
    </html>"""


# Store for active pipeline runs with their status queues
_active_runs = {}


def _run_pipeline_with_status(config: dict, status_queue: Queue):
    """Run pipeline in a thread, pushing status updates to a queue."""
    def status_callback(stage: str, message: str, current: int = None, total: int = None):
        status_queue.put({
            "stage": stage,
            "message": message,
            "current": current,
            "total": total
        })
    
    try:
        result = run_pipeline(config, status_callback=status_callback)
        status_queue.put({"stage": "complete", "message": "Pipeline complete", "result": result})
    except Exception as e:
        status_queue.put({"stage": "error", "message": str(e), "error": True})


@app.get("/runs/{run_id}/status")
async def stream_run_status(run_id: str):
    """SSE endpoint for streaming pipeline status updates."""
    if run_id not in _active_runs:
        raise HTTPException(status_code=404, detail="Run not found")
    
    status_queue = _active_runs[run_id]
    
    async def event_generator():
        while True:
            # Check for new status updates
            if not status_queue.empty():
                status = status_queue.get()
                yield f"data: {json.dumps(status)}\n\n"
                
                # If complete or error, stop streaming
                if status.get("stage") in ("complete", "error"):
                    del _active_runs[run_id]
                    break
            else:
                # Send keepalive
                yield ": keepalive\n\n"
            
            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


def _progress_page_html(run_id: str) -> str:
    """Generate HTML for the progress page with SSE updates."""
    return f"""<!doctype html>
    <html>
    <head>
      <title>Pipeline Running - {run_id[:8]}</title>
      <style>
        :root {{
          --bg: #0f172a;
          --bg-card: #020617;
          --accent: #22c55e;
          --text: #e5e7eb;
          --muted: #9ca3af;
        }}
        body {{
          margin: 0;
          min-height: 100vh;
          font-family: system-ui, -apple-system, sans-serif;
          background: radial-gradient(circle at top left, #1e293b 0, #020617 40%);
          color: var(--text);
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .container {{
          max-width: 600px;
          width: 100%;
          padding: 2rem;
        }}
        h1 {{
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }}
        .run-id {{
          color: var(--muted);
          font-size: 0.9rem;
          margin-bottom: 2rem;
        }}
        .status-card {{
          background: var(--bg-card);
          border: 1px solid rgba(148,163,184,0.35);
          border-radius: 0.75rem;
          padding: 1.5rem;
          margin-bottom: 1rem;
        }}
        .stage {{
          font-size: 0.8rem;
          text-transform: uppercase;
          color: var(--accent);
          margin-bottom: 0.5rem;
        }}
        .message {{
          font-size: 1rem;
          margin-bottom: 1rem;
        }}
        .progress-bar {{
          background: rgba(148,163,184,0.2);
          border-radius: 0.25rem;
          height: 8px;
          overflow: hidden;
        }}
        .progress-fill {{
          background: linear-gradient(90deg, var(--accent), #4ade80);
          height: 100%;
          width: 0%;
          transition: width 0.3s ease;
        }}
        .log {{
          background: rgba(0,0,0,0.3);
          border-radius: 0.5rem;
          padding: 1rem;
          max-height: 200px;
          overflow-y: auto;
          font-family: monospace;
          font-size: 0.8rem;
          color: var(--muted);
        }}
        .log-entry {{
          margin-bottom: 0.25rem;
        }}
        .complete {{
          color: var(--accent);
        }}
        .error {{
          color: #ef4444;
        }}
        a {{
          color: var(--accent);
        }}
        .hidden {{
          display: none;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Pipeline Running</h1>
        <p class="run-id">Run ID: {run_id}</p>
        
        <div class="status-card">
          <div class="stage" id="stage">Initializing...</div>
          <div class="message" id="message">Starting pipeline...</div>
          <div class="progress-bar">
            <div class="progress-fill" id="progress"></div>
          </div>
        </div>
        
        <div class="log" id="log"></div>
        
        <p id="result-link" class="hidden">
          <a href="/runs/{run_id}/summary">View Results →</a>
        </p>
      </div>
      
      <script>
        const runId = "{run_id}";
        const stageEl = document.getElementById('stage');
        const messageEl = document.getElementById('message');
        const progressEl = document.getElementById('progress');
        const logEl = document.getElementById('log');
        const resultLink = document.getElementById('result-link');
        
        const eventSource = new EventSource('/runs/' + runId + '/status');
        
        eventSource.onmessage = function(event) {{
          const data = JSON.parse(event.data);
          
          // Update stage
          stageEl.textContent = data.stage || 'Processing';
          stageEl.className = 'stage' + (data.stage === 'complete' ? ' complete' : '') + (data.error ? ' error' : '');
          
          // Update message
          messageEl.textContent = data.message || '';
          
          // Update progress bar
          if (data.current && data.total) {{
            const pct = Math.round((data.current / data.total) * 100);
            progressEl.style.width = pct + '%';
          }}
          
          // Add to log
          const logEntry = document.createElement('div');
          logEntry.className = 'log-entry';
          logEntry.textContent = '[' + data.stage + '] ' + data.message;
          logEl.appendChild(logEntry);
          logEl.scrollTop = logEl.scrollHeight;
          
          // Handle completion
          if (data.stage === 'complete') {{
            eventSource.close();
            resultLink.classList.remove('hidden');
            progressEl.style.width = '100%';
          }}
          
          // Handle error
          if (data.error) {{
            eventSource.close();
            messageEl.classList.add('error');
          }}
        }};
        
        eventSource.onerror = function() {{
          stageEl.textContent = 'Connection lost';
          stageEl.className = 'stage error';
        }};
      </script>
    </body>
    </html>"""


@app.post("/runs/gcs")
async def start_run_gcs(
    request: Request,
    bucket: str = Form(...),
    project: Optional[str] = Form(None),
    archive_bucket: Optional[str] = Form(None),
    skip_analysis: bool = Form(False),
    categorize: bool = Form(False),
    translate: bool = Form(False),
    validate: bool = Form(False),
):
    run_id = str(uuid.uuid4())
    
    config = {
        "source_type": "gcs",
        "bucket": bucket,
        "project": project,
        "archive_bucket": archive_bucket,
        "skip_analysis": skip_analysis,
        "categorize": categorize,
        "translate": translate,
        "validate": validate,
        "run_id": run_id,
    }

    # If client explicitly wants JSON, run synchronously
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        result = run_pipeline(config)
        return JSONResponse(result)

    # Start pipeline in background thread with status queue
    status_queue = Queue()
    _active_runs[run_id] = status_queue
    
    thread = Thread(target=_run_pipeline_with_status, args=(config, status_queue))
    thread.daemon = True
    thread.start()

    # Return progress page
    return HTMLResponse(content=_progress_page_html(run_id))


@app.post("/runs/local")
async def start_run_local(
    request: Request,
    files: List[UploadFile] = File(...),
    project: Optional[str] = Form(None),
    archive_bucket: Optional[str] = Form(None),
    skip_analysis: bool = Form(False),
    categorize: bool = Form(False),
    translate: bool = Form(False),
    validate: bool = Form(False),
):
    run_id = str(uuid.uuid4())
    
    input_dir = "input"
    os.makedirs(input_dir, exist_ok=True)

    local_paths = []
    for f in files:
        dest_path = os.path.join(input_dir, f.filename)
        content = await f.read()
        with open(dest_path, "wb") as out:
            out.write(content)
        local_paths.append(dest_path)

    config = {
        "source_type": "local",
        "local_files": local_paths,
        "project": project,
        "archive_bucket": archive_bucket,
        "skip_analysis": skip_analysis,
        "categorize": categorize,
        "translate": translate,
        "validate": validate,
        "run_id": run_id,
    }

    # If client explicitly wants JSON, run synchronously
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        result = run_pipeline(config)
        return JSONResponse(result)

    # Start pipeline in background thread with status queue
    status_queue = Queue()
    _active_runs[run_id] = status_queue
    
    thread = Thread(target=_run_pipeline_with_status, args=(config, status_queue))
    thread.daemon = True
    thread.start()

    # Return progress page
    return HTMLResponse(content=_progress_page_html(run_id))


@app.get("/runs/{run_id}/summary")
async def run_summary(request: Request, run_id: str):
    """Return a summary of artefacts for a given run.

    For browser clients, this returns an HTML page with clickable links.
    For API clients (Accept: application/json), it returns JSON.
    """
    output_dir = os.path.join(BASE_OUTPUT_ROOT, run_id)
    if not os.path.isdir(output_dir):
        raise HTTPException(status_code=404, detail="Run not found")

    def _maybe(path: str) -> Optional[str]:
        return path if os.path.exists(path) else None

    analysis_json = _maybe(os.path.join(output_dir, "analysis_results.json"))
    analysis_report = _maybe(os.path.join(output_dir, "analysis_report.txt"))
    dependency_graph = _maybe(os.path.join(output_dir, "dependency_graph.mmd"))
    categorization_json = _maybe(os.path.join(output_dir, "data_categorization.json"))
    categorization_report = _maybe(os.path.join(output_dir, "categorization_report.txt"))
    validation_tests = _maybe(os.path.join(output_dir, "validation_tests.json"))
    validation_report = _maybe(os.path.join(output_dir, "validation_report.txt"))
    type_mapping_report = _maybe(os.path.join(output_dir, "type_mapping_report.txt"))

    dataform_dir = os.path.join(output_dir, "dataform")
    has_dataform = os.path.isdir(dataform_dir)

    def _download_url(abs_path: Optional[str]) -> Optional[str]:
        if not abs_path:
            return None
        rel = os.path.relpath(abs_path, output_dir)
        return f"/runs/{run_id}/files/{rel}".replace("\\", "/")

    artefacts = {
        "analysis_results": _download_url(analysis_json),
        "analysis_report": _download_url(analysis_report),
        "dependency_graph": _download_url(dependency_graph),
        "categorization_results": _download_url(categorization_json),
        "categorization_report": _download_url(categorization_report),
        "validation_tests": _download_url(validation_tests),
        "validation_report": _download_url(validation_report),
        "type_mapping_report": _download_url(type_mapping_report),
        "dataform_root": f"/runs/{run_id}/files/dataform" if has_dataform else None,
    }

    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return JSONResponse({"run_id": run_id, "artefacts": artefacts})

    # Simple HTML summary page
    def _row(label: str, key: str) -> str:
        url = artefacts.get(key)
        if not url:
            return f"<tr><td>{label}</td><td><em>Not generated</em></td></tr>"
        return f"<tr><td>{label}</td><td><a href='{url}'>{url}</a></td></tr>"

    rows = "".join(
        [
            _row("Analysis results (JSON)", "analysis_results"),
            _row("Analysis report", "analysis_report"),
            _row("Dependency graph (Mermaid)", "dependency_graph"),
            _row("Categorisation results (JSON)", "categorization_results"),
            _row("Categorisation report", "categorization_report"),
            _row("Validation tests (JSON)", "validation_tests"),
            _row("Validation report", "validation_report"),
            _row("Type mapping report", "type_mapping_report"),
            _row("Dataform project root", "dataform_root"),
        ]
    )

    html = f"""<!doctype html>
    <html>
    <head>
      <title>Run summary - {run_id}</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        h1 {{ margin-bottom: 0.5rem; }}
        table {{ border-collapse: collapse; margin-top: 1rem; }}
        th, td {{ border: 1px solid #e5e7eb; padding: 0.4rem 0.6rem; }}
        th {{ background: #f3f4f6; text-align: left; }}
        a {{ color: #1565c0; }}
        em {{ color: #6b7280; }}
      </style>
    </head>
    <body>
      <h1>Run summary</h1>
      <p><strong>Run ID:</strong> {run_id}</p>
      <table>
        <thead>
          <tr><th>Artefact</th><th>Link</th></tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
      <p><a href="/">Back to start</a></p>
    </body>
    </html>"""

    return HTMLResponse(content=html)


@app.get("/runs/{run_id}/files/{path:path}")
async def download_run_file(run_id: str, path: str):
    """Serve a file from a given run's output directory.

    This is a simple convenience for accessing artefacts from the browser.
    """
    output_dir = os.path.join(BASE_OUTPUT_ROOT, run_id)
    full_path = os.path.normpath(os.path.join(output_dir, path))

    # Use absolute paths to prevent directory traversal outside the run directory
    abs_output = os.path.abspath(output_dir)
    abs_full = os.path.abspath(full_path)
    if not abs_full.startswith(abs_output + os.sep) and abs_full != abs_output:
        raise HTTPException(status_code=400, detail="Invalid path")

    if not os.path.exists(abs_full):
        raise HTTPException(status_code=404, detail="File not found")

    # If the path is a directory, return a simple listing so users can
    # browse the generated Dataform project and other artefacts.
    if os.path.isdir(abs_full):
        entries = sorted(os.listdir(abs_full))
        # Basic HTML directory listing
        links = []
        for name in entries:
            child_rel = os.path.relpath(os.path.join(abs_full, name), output_dir).replace("\\", "/")
            links.append(f"<li><a href='/runs/{run_id}/files/{child_rel}'>{name}</a></li>")
        html = f"""<!doctype html>
        <html>
        <head>
          <title>Files for run {run_id}</title>
          <style>
            body {{ font-family: Arial, sans-serif; margin: 2rem; }}
            a {{ color: #1565c0; }}
          </style>
        </head>
        <body>
          <h1>Files under {path or '.'}</h1>
          <ul>
            {''.join(links)}
          </ul>
          <p><a href="/runs/{run_id}/summary">Back to run summary</a></p>
        </body>
        </html>"""
        return HTMLResponse(content=html)

    filename = os.path.basename(abs_full)
    return FileResponse(abs_full, filename=filename)
