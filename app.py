import os
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
        body { font-family: Arial, sans-serif; margin: 2rem; }
        h1 { margin-bottom: 0.5rem; }
        h2 { margin-top: 2rem; }
        form { margin-bottom: 2rem; padding: 1rem; border: 1px solid #ccc; }
        label { display: block; margin-top: 0.5rem; }
      </style>
    </head>
    <body>
      <h1>Sybase to BigQuery Agentic Migration</h1>

      <h2>Run using GCS bucket</h2>
      <form action="/runs/gcs" method="post">
        <label>GCS Bucket:
          <input type="text" name="bucket" value="crown-poc" required />
        </label>
        <label>GCP Project ID:
          <input type="text" name="project" value="gcp-sandpit-intelia" />
        </label>
        <label>
          <input type="checkbox" name="skip_analysis" value="true" />
          Skip analysis (reuse existing analysis_results.json for this run_id if configured)
        </label>
        <label>
          <input type="checkbox" name="categorize" value="true" checked />
          Run data categorization
        </label>
        <label>
          <input type="checkbox" name="translate" value="true" checked />
          Run schema translation to Dataform
        </label>
        <label>
          <input type="checkbox" name="validate" value="true" checked />
          Generate validation tests
        </label>
        <button type="submit">Start GCS Run</button>
      </form>

      <h2>Run using local file upload</h2>
      <form action="/runs/local" method="post" enctype="multipart/form-data">
        <label>Files (Sybase DDL/SP .sql, Informatica .xml, etc.):
          <input type="file" name="files" multiple required />
        </label>
        <label>GCP Project ID:
          <input type="text" name="project" value="gcp-sandpit-intelia" />
        </label>
        <label>
          <input type="checkbox" name="skip_analysis" value="true" />
          Skip analysis (not usually needed for uploads)
        </label>
        <label>
          <input type="checkbox" name="categorize" value="true" checked />
          Run data categorization
        </label>
        <label>
          <input type="checkbox" name="translate" value="true" checked />
          Run schema translation to Dataform
        </label>
        <label>
          <input type="checkbox" name="validate" value="true" checked />
          Generate validation tests
        </label>
        <button type="submit">Start Local Run</button>
      </form>

      <p>
        After a run completes, note the <code>run_id</code> from the JSON response
        and open <code>/runs/&lt;run_id&gt;/summary</code> to view download links
        for the key artefacts.
      </p>
    </body>
    </html>"""


@app.post("/runs/gcs")
async def start_run_gcs(
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
    return JSONResponse(result)


@app.post("/runs/local")
async def start_run_local(
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
    return JSONResponse(result)
