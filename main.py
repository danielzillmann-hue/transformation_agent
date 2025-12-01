import argparse
from src.service import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Sybase to BigQuery Agentic Migration Framework")
    parser.add_argument("--bucket", default="crown-poc", help="GCS bucket name")
    parser.add_argument("--project", help="GCP Project ID")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip analysis and use existing JSON results")
    parser.add_argument("--categorize", action="store_true", help="Run data categorization after analysis")
    parser.add_argument("--translate", action="store_true", help="Run schema translation to BigQuery/Dataform")
    parser.add_argument("--validate", action="store_true", help="Generate validation test cases from analysis results")
    args = parser.parse_args()

    config = {
        "source_type": "gcs",
        "bucket": args.bucket,
        "project": args.project,
        "skip_analysis": args.skip_analysis,
        "categorize": args.categorize,
        "translate": args.translate,
        "validate": args.validate,
    }

    run_pipeline(config)

if __name__ == "__main__":
    main()
