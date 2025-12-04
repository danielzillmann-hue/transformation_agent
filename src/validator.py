import json
import os
import logging

from src.llm_client import LLMClient
from src.prompts import VALIDATION_TEST_PROMPT
from src.json_utils import safe_parse_json

logger = logging.getLogger(__name__)


class ValidationEngine:
    def __init__(self, project_id="dan-sandpit", output_dir="output"):
        self.output_dir = output_dir
        self.llm_client = LLMClient(project_id)
        os.makedirs(output_dir, exist_ok=True)

    def validate(self, analysis_results, status_callback=None):
        """Generates validation test definitions from analysis results.

        This initial implementation does not execute tests against Sybase/BigQuery.
        It focuses on generating structured test cases and a human-readable report
        that can later be wired into automated execution.
        """
        logger.info("Starting validation & test generation...")
        
        if status_callback:
            status_callback("validation", "Generating validation test cases...", 1, 3)

        test_definitions = {}

        for filename, data in analysis_results.items():
            analysis_text = data.get("analysis", "")
            if not analysis_text or analysis_text.startswith("Error"):
                continue

            # Use safe JSON parsing with repair
            info = safe_parse_json(analysis_text)
            if not info:
                logger.warning(f"Skipping {filename} for validation, could not parse JSON")
                continue

            # Determine object type for prompt context
            object_type = "table" if "table_name" in info else "procedure" if "procedure_name" in info else "mapping" if "mapping_name" in info else "unknown"

            prompt = VALIDATION_TEST_PROMPT.format(object_type=object_type, analysis=json.dumps(info, indent=2))
            response = self.llm_client.generate_content(prompt)

            # Use safe JSON parsing with repair for LLM response
            tests = safe_parse_json(response)
            if not tests:
                logger.warning(f"Failed to parse validation tests for {filename}")
                continue
            
            test_definitions[filename] = {
                "object_type": object_type,
                "tests": tests,
            }

        if status_callback:
            status_callback("validation", "Saving validation results...", 2, 3)
        
        self._save_results(test_definitions)
        
        if status_callback:
            status_callback("validation", "Generating validation report...", 3, 3)
        
        self._generate_report(test_definitions)

        logger.info("Validation & test generation complete.")

    def _save_results(self, test_definitions):
        """Save validation test definitions to JSON."""
        output_path = os.path.join(self.output_dir, "validation_tests.json")
        with open(output_path, "w") as f:
            json.dump(test_definitions, f, indent=2)
        logger.info(f"Saved validation test definitions to {output_path}")

    def _generate_report(self, test_definitions):
        """Generate a text validation summary report."""
        report_path = os.path.join(self.output_dir, "validation_report.txt")

        with open(report_path, "w") as f:
            f.write("Validation & Testing Report\n\n")

            total_objects = len(test_definitions)
            total_tests = sum(len(obj.get("tests", {}).get("test_cases", [])) for obj in test_definitions.values())

            f.write("Summary\n\n")
            f.write(f"Objects with tests: {total_objects}\n")
            f.write(f"Total test cases generated: {total_tests}\n\n")
            f.write(f"- **Total test cases generated**: {total_tests}\n\n")

            for filename, obj in test_definitions.items():
                object_type = obj.get("object_type", "unknown")
                tests = obj.get("tests", {})
                name = tests.get("object_name") or filename

                f.write(f"## {name} ({object_type})\n\n")

                # High-level summary if provided
                if "summary" in tests:
                    f.write(f"{tests['summary']}\n\n")

                # Table / object metadata
                if "metadata" in tests:
                    f.write("### Metadata\n\n")
                    for key, value in tests["metadata"].items():
                        f.write(f"- **{key}**: {value}\n")
                    f.write("\n")

                # Individual test cases
                cases = tests.get("test_cases", [])
                if cases:
                    f.write("### Test Cases\n\n")
                    for idx, case in enumerate(cases, start=1):
                        f.write(f"#### Test {idx}: {case.get('name', 'Unnamed test')}\n\n")
                        if case.get("description"):
                            f.write(f"{case['description']}\n\n")
                        if case.get("sql"):
                            f.write("```sql\n")
                            f.write(case["sql"])
                            f.write("\n```\n\n")
                        if case.get("expected"):
                            f.write("**Expected:**\n\n")
                            f.write(f"{json.dumps(case['expected'], indent=2)}\n\n")

        logger.info(f"Generated validation report at {report_path}")
