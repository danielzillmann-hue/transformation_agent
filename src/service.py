import logging
import os
import uuid

from src.ingestion import IngestionEngine
from src.analyzer import AnalysisEngine
from src.reporter import Reporter
from src.visualizer import Visualizer
from src.categorizer import DataCategorizer
from src.translator import SchemaTranslator
from src.validator import ValidationEngine


logger = logging.getLogger(__name__)


class LocalBlob:
    def __init__(self, path: str):
        self._path = path
        self.name = os.path.basename(path)

    def download_as_text(self) -> str:
        with open(self._path, "r", encoding="utf-8") as f:
            return f.read()


def run_pipeline(config: dict) -> dict:
    source_type = config.get("source_type", "gcs")
    bucket = config.get("bucket")
    local_files = config.get("local_files", [])
    project_id = config.get("project") or "gcp-sandpit-intelia"
    skip_analysis = config.get("skip_analysis", False)
    do_categorize = config.get("categorize", False)
    do_translate = config.get("translate", False)
    do_validate = config.get("validate", False)

    run_id = config.get("run_id") or str(uuid.uuid4())

    logging.basicConfig(level=logging.INFO)
    logger.info("Starting pipeline %s with config: %s", run_id, config)

    results = {}
    base_output_root = config.get("output_root", "runs")
    output_dir = os.path.join(base_output_root, run_id)
    os.makedirs(output_dir, exist_ok=True)

    analysis_json_path = os.path.join(output_dir, "analysis_results.json")

    if skip_analysis and os.path.exists(analysis_json_path):
        import json

        logger.info("Skipping analysis, loading results from JSON: %s", analysis_json_path)
        with open(analysis_json_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        if source_type == "gcs":
            if not bucket:
                raise ValueError("bucket is required when source_type is 'gcs'")
            ingestion = IngestionEngine(bucket)
            files = ingestion.list_files()
            logger.info("Found %d files in bucket %s", len(files), bucket)
        elif source_type == "local":
            if not local_files:
                raise ValueError("local_files must be provided when source_type is 'local'")
            files = [LocalBlob(path) for path in local_files]
            logger.info("Using %d local files for analysis", len(files))
        else:
            raise ValueError(f"Unsupported source_type: {source_type}")

        analyzer = AnalysisEngine(project_id=project_id)
        results = analyzer.analyze(files)

    reporter = Reporter(output_dir=output_dir)
    reporter.generate_report(results)

    visualizer = Visualizer(output_dir=output_dir)
    visualizer.generate_dependency_diagram(results)

    categorization_results = None
    categorization_json_path = os.path.join(output_dir, "data_categorization.json")

    if do_categorize:
        categorizer = DataCategorizer(project_id=project_id, output_dir=output_dir)
        categorizer.categorize(results)

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

        translator = SchemaTranslator(project_id=project_id, output_dir=output_dir)
        translator.translate(results, categorization_results)

    if do_validate:
        validator = ValidationEngine(project_id=project_id, output_dir=output_dir)
        validator.validate(results)

    dataform_dir = os.path.join(output_dir, "dataform") if os.path.isdir(os.path.join(output_dir, "dataform")) else None
    validation_tests_path = os.path.join(output_dir, "validation_tests.json") if os.path.exists(os.path.join(output_dir, "validation_tests.json")) else None
    validation_report_path = os.path.join(output_dir, "validation_report.md") if os.path.exists(os.path.join(output_dir, "validation_report.md")) else None

    return {
        "run_id": run_id,
        "output_dir": output_dir,
        "analysis_results_path": analysis_json_path if os.path.exists(analysis_json_path) else None,
        "analysis_report_path": os.path.join(output_dir, "analysis_report.md"),
        "dependency_graph_path": os.path.join(output_dir, "dependency_graph.mmd"),
        "categorization_path": categorization_json_path if os.path.exists(categorization_json_path) else None,
        "categorization_report_path": os.path.join(output_dir, "categorization_report.md") if os.path.exists(os.path.join(output_dir, "categorization_report.md")) else None,
        "dataform_dir": dataform_dir,
        "validation_tests_path": validation_tests_path,
        "validation_report_path": validation_report_path,
    }
