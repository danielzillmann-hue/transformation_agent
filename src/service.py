import logging
import os
import uuid
import shutil
from typing import Callable, Optional

from src.ingestion import IngestionEngine
from src.analyzer import AnalysisEngine
from src.reporter import Reporter
from src.visualizer import Visualizer
from src.categorizer import DataCategorizer
from src.translator import SchemaTranslator
from src.validator import ValidationEngine
from google.cloud import storage


logger = logging.getLogger(__name__)

# Type alias for status callback
StatusCallback = Callable[[str, str, Optional[int], Optional[int]], None]


def _noop_status(stage: str, message: str, current: int = None, total: int = None):
    """Default no-op status callback."""
    pass


class LocalBlob:
    def __init__(self, path: str):
        self._path = path
        self.name = os.path.basename(path)

    def download_as_text(self) -> str:
        # Try UTF-8 first, fall back to latin-1 for files with special characters
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(self._path, "r", encoding="latin-1") as f:
                return f.read()


def run_pipeline(config: dict, status_callback: StatusCallback = None) -> dict:
    """Run the transformation pipeline with optional status updates.
    
    Args:
        config: Pipeline configuration dictionary
        status_callback: Optional callback function(stage, message, current, total)
                        for progress updates
    """
    status = status_callback or _noop_status
    
    source_type = config.get("source_type", "gcs")
    bucket = config.get("bucket")
    local_files = config.get("local_files", [])
    project_id = config.get("project") or "dan-sandpit"
    source_system = config.get("source_system")  # e.g., 'sybase', 'oracle', 'sqlserver'
    skip_analysis = config.get("skip_analysis", False)
    do_categorize = config.get("categorize", False)
    do_translate = config.get("translate", False)
    do_validate = config.get("validate", False)
    archive_bucket = config.get("archive_bucket")

    run_id = config.get("run_id") or str(uuid.uuid4())

    logging.basicConfig(level=logging.INFO)
    logger.info("Starting pipeline %s with config: %s", run_id, config)
    status("init", f"Starting pipeline run {run_id[:8]}...")

    results = {}
    base_output_root = config.get("output_root", "runs")
    output_dir = os.path.join(base_output_root, run_id)
    os.makedirs(output_dir, exist_ok=True)

    analysis_json_path = os.path.join(output_dir, "analysis_results.json")

    if skip_analysis and os.path.exists(analysis_json_path):
        import json

        logger.info("Skipping analysis, loading results from JSON: %s", analysis_json_path)
        status("analysis", "Loading cached analysis results...")
        with open(analysis_json_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        status("analysis", f"Loaded {len(results)} cached results")
    else:
        if source_type == "gcs":
            if not bucket:
                raise ValueError("bucket is required when source_type is 'gcs'")
            status("ingestion", f"Connecting to GCS bucket: {bucket}")
            ingestion = IngestionEngine(bucket)
            files = ingestion.list_files()
            logger.info("Found %d files in bucket %s", len(files), bucket)
            status("ingestion", f"Found {len(files)} files in bucket")
        elif source_type == "local":
            if not local_files:
                raise ValueError("local_files must be provided when source_type is 'local'")
            files = [LocalBlob(path) for path in local_files]
            logger.info("Using %d local files for analysis", len(files))
            status("ingestion", f"Loaded {len(files)} local files")
        else:
            raise ValueError(f"Unsupported source_type: {source_type}")

        status("analysis", f"Analyzing {len(files)} files with LLM...")
        analyzer = AnalysisEngine(project_id=project_id, source_system=source_system)
        results = analyzer.analyze(files, status_callback=status)

    status("reporting", "Generating analysis report...")
    reporter = Reporter(output_dir=output_dir, source_system=source_system)
    reporter.generate_report(results)

    status("visualization", "Creating dependency diagram...")
    visualizer = Visualizer(output_dir=output_dir)
    visualizer.generate_dependency_diagram(results)

    categorization_results = None
    categorization_json_path = os.path.join(output_dir, "data_categorization.json")

    if do_categorize:
        status("categorization", "Categorizing data by business domain...")
        categorizer = DataCategorizer(project_id=project_id, output_dir=output_dir, source_system=source_system)
        categorizer.categorize(results, status_callback=status)

        import json

        if os.path.exists(categorization_json_path):
            with open(categorization_json_path, "r", encoding="utf-8") as f:
                categorization_results = json.load(f)

    if do_translate:
        if not categorization_results:
            import json

            if os.path.exists(categorization_json_path):
                with open(categorization_json_path, "r", encoding="utf-8") as f:
                    categorization_results = json.load(f)
            else:
                categorization_results = {"domains": [], "categorizations": {}}

        status("translation", "Translating schemas to BigQuery/Dataform...")
        translator = SchemaTranslator(project_id=project_id, output_dir=output_dir, source_system=source_system)
        translator.translate(results, categorization_results, status_callback=status)

    if do_validate:
        status("validation", "Generating validation test cases...")
        validator = ValidationEngine(project_id=project_id, output_dir=output_dir, source_system=source_system)
        validator.validate(results, status_callback=status)

    dataform_dir = os.path.join(output_dir, "dataform") if os.path.isdir(os.path.join(output_dir, "dataform")) else None
    validation_tests_path = os.path.join(output_dir, "validation_tests.json") if os.path.exists(os.path.join(output_dir, "validation_tests.json")) else None
    validation_report_path = os.path.join(output_dir, "validation_report.txt") if os.path.exists(os.path.join(output_dir, "validation_report.txt")) else None

    analysis_report_path = os.path.join(output_dir, "analysis_report.txt") if os.path.exists(os.path.join(output_dir, "analysis_report.txt")) else None
    categorization_report_path = os.path.join(output_dir, "categorization_report.txt") if os.path.exists(os.path.join(output_dir, "categorization_report.txt")) else None

    gcs_uris = {}
    if archive_bucket:
        try:
            client = storage.Client(project=project_id)
            bucket_obj = client.bucket(archive_bucket)
            base_prefix = f"runs/{run_id}/"

            def _upload(local_path, rel_name=None):
                if not local_path or not os.path.exists(local_path):
                    return None
                rel = rel_name or os.path.basename(local_path)
                blob_path = base_prefix + rel
                blob = bucket_obj.blob(blob_path)
                blob.upload_from_filename(local_path)
                return f"gs://{archive_bucket}/{blob_path}"

            gcs_uris["analysis_results_uri"] = _upload(analysis_json_path, "analysis_results.json")
            gcs_uris["analysis_report_uri"] = _upload(analysis_report_path, "analysis_report.txt")
            gcs_uris["dependency_graph_uri"] = _upload(os.path.join(output_dir, "dependency_graph.mmd"), "dependency_graph.mmd")
            gcs_uris["categorization_uri"] = _upload(categorization_json_path, "data_categorization.json")
            gcs_uris["categorization_report_uri"] = _upload(categorization_report_path, "categorization_report.txt")
            gcs_uris["validation_tests_uri"] = _upload(validation_tests_path, "validation_tests.json")
            gcs_uris["validation_report_uri"] = _upload(validation_report_path, "validation_report.txt")

            if dataform_dir and os.path.isdir(dataform_dir):
                archive_base = os.path.join(output_dir, "dataform")
                zip_path = shutil.make_archive(archive_base, "zip", dataform_dir)
                gcs_uris["dataform_zip_uri"] = _upload(zip_path, "dataform.zip")
        except Exception as e:
            logger.warning("Failed to archive artefacts to GCS: %s", e)

    result = {
        "run_id": run_id,
        "output_dir": output_dir,
        "analysis_results_path": analysis_json_path if os.path.exists(analysis_json_path) else None,
        "analysis_report_path": analysis_report_path,
        "dependency_graph_path": os.path.join(output_dir, "dependency_graph.mmd"),
        "categorization_path": categorization_json_path if os.path.exists(categorization_json_path) else None,
        "categorization_report_path": categorization_report_path,
        "dataform_dir": dataform_dir,
        "validation_tests_path": validation_tests_path,
        "validation_report_path": validation_report_path,
    }

    if gcs_uris:
        result["gcs_uris"] = gcs_uris

    return result
