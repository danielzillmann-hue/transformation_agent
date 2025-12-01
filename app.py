import os
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse

from src.service import run_pipeline

app = FastAPI(title="Sybase to BigQuery Agentic Migration API")

BASE_OUTPUT_ROOT = "runs"


@app.get("/", response_class=HTMLResponse)
async def index():
    return """<!doctype html>
    <html>
    <head>
      <title>Sybase to BigQuery Agentic Migration</title>
      <style>
        :root {
          color-scheme: light dark;
          --bg: #0f172a;
          --bg-card: #020617;
          --border-subtle: rgba(148, 163, 184, 0.4);
          --accent: #22c55e;
          --accent-soft: rgba(34, 197, 94, 0.16);
          --text: #e5e7eb;
          --muted: #9ca3af;
        }
        body {
          margin: 0;
          min-height: 100vh;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: radial-gradient(circle at top left, #1e293b 0, #020617 40%, #020617 100%);
          color: var(--text);
          display: flex;
          align-items: stretch;
          justify-content: center;
        }
        .shell {
          max-width: 1100px;
          width: 100%;
          padding: 2.5rem 1.5rem 3rem;
        }
        .header {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-bottom: 2rem;
        }
        .title-row {
          display: flex;
          align-items: center;
          gap: 0.6rem;
        }
        .pill {
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          padding: 0.18rem 0.55rem;
          border-radius: 999px;
          border: 1px solid var(--border-subtle);
          color: var(--muted);
        }
        h1 {
          font-size: 1.6rem;
          font-weight: 600;
          margin: 0;
        }
        .subtitle {
          font-size: 0.95rem;
          color: var(--muted);
          max-width: 640px;
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
          gap: 1.25rem;
        }
        .card {
          background: radial-gradient(circle at top left, rgba(34,197,94,0.05), #020617 55%);
          border-radius: 0.9rem;
          border: 1px solid rgba(148,163,184,0.35);
          padding: 1.4rem 1.4rem 1.5rem;
          box-shadow: 0 18px 45px rgba(15,23,42,0.85);
        }
        .card h2 {
          font-size: 1.05rem;
          margin: 0 0 0.4rem;
        }
        .card p {
          margin: 0 0 0.9rem;
          font-size: 0.9rem;
          color: var(--muted);
        }
        form {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-top: 0.5rem;
        }
        label {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          font-size: 0.8rem;
          color: var(--muted);
        }
        input[type="text"], input[type="file"] {
          border-radius: 0.45rem;
          border: 1px solid rgba(148,163,184,0.55);
          padding: 0.45rem 0.6rem;
          background: rgba(15,23,42,0.85);
          color: var(--text);
          font-size: 0.85rem;
        }
        input[type="file"] {
          padding: 0.35rem 0.6rem;
        }
        input[type="checkbox"] {
          accent-color: var(--accent);
        }
        .inline-option {
          display: flex;
          align-items: center;
          gap: 0.45rem;
          font-size: 0.8rem;
          color: var(--muted);
        }
        button[type="submit"] {
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
        }
        button[type="submit"]:hover {
          filter: brightness(1.05);
        }
        .footer-note {
          margin-top: 1.6rem;
          font-size: 0.8rem;
          color: var(--muted);
        }
        code {
          background: rgba(15,23,42,0.9);
          padding: 0.1rem 0.35rem;
          border-radius: 0.25rem;
        }
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
                <input type="text" name="bucket" value="crownpoc" required />
              </label>
              <label>GCP Project ID
                <input type="text" name="project" value="dan-sandpit" />
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


@app.post("/runs/gcs")
async def start_run_gcs(
    request: Request,
    bucket: str = Form(...),
    project: Optional[str] = Form(None),
    skip_analysis: bool = Form(False),
    categorize: bool = Form(False),
    translate: bool = Form(False),
    validate: bool = Form(False),
):
    config = {
        "source_type": "gcs",
        "bucket": bucket,
        "project": project,
        "skip_analysis": skip_analysis,
        "categorize": categorize,
        "translate": translate,
        "validate": validate,
    }

    result = run_pipeline(config)

    # If client explicitly wants JSON, return JSON
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return JSONResponse(result)

    run_id = result.get("run_id")
    summary_url = f"/runs/{run_id}/summary" if run_id else "#"

    # Simple HTML results page with link to summary
    html = f"""<!doctype html>
    <html>
    <head>
      <title>GCS Run Started</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        a {{ color: #1565c0; }}
      </style>
    </head>
    <body>
      <h1>Run started from GCS bucket</h1>
      <p><strong>Run ID:</strong> {run_id}</p>
      <p>View artefact links: <a href="{summary_url}">{summary_url}</a></p>
      <p><a href="/">Back to start</a></p>
    </body>
    </html>"""

    return HTMLResponse(content=html)


@app.post("/runs/local")
async def start_run_local(
    request: Request,
    files: List[UploadFile] = File(...),
    project: Optional[str] = Form(None),
    skip_analysis: bool = Form(False),
    categorize: bool = Form(False),
    translate: bool = Form(False),
    validate: bool = Form(False),
):
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
        "skip_analysis": skip_analysis,
        "categorize": categorize,
        "translate": translate,
        "validate": validate,
    }

    result = run_pipeline(config)

    # If client explicitly wants JSON, return JSON
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return JSONResponse(result)

    run_id = result.get("run_id")
    summary_url = f"/runs/{run_id}/summary" if run_id else "#"

    html = f"""<!doctype html>
    <html>
    <head>
      <title>Local Run Started</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        a {{ color: #1565c0; }}
      </style>
    </head>
    <body>
      <h1>Run started from uploaded files</h1>
      <p><strong>Run ID:</strong> {run_id}</p>
      <p>View artefact links: <a href="{summary_url}">{summary_url}</a></p>
      <p><a href="/">Back to start</a></p>
    </body>
    </html>"""

    return HTMLResponse(content=html)
