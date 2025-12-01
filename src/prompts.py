SCHEMA_ANALYSIS_PROMPT = """
You are a Sybase Database Expert. Analyze the following DDL statement.
Extract the following information in JSON format:
- table_name
- columns (list of objects with name, type, nullable)
- primary_keys (list of column names)
- foreign_keys (list of objects with column, referenced_table, referenced_column)
- constraints (list of strings)

DDL:
{content}
"""

SP_ANALYSIS_PROMPT = """
You are a Sybase Database Expert. Analyze the following Stored Procedure.
Extract the following information in JSON format:
- procedure_name
- parameters (list of objects with name, type, mode)
- logic_summary (text description of what the SP does)
- tables_read (list of table names)
- tables_modified (list of table names)
- dependencies (list of other SPs or views called)

Stored Procedure:
{content}
"""

INFORMATICA_ANALYSIS_PROMPT = """
You are an ETL Expert. Analyze the following Informatica XML export.
Extract the following information in JSON format:
- mapping_name
- sources (list of source table/file names)
- targets (list of target table/file names)
- transformations (list of objects with type, description)
- logic_summary (text description of the data flow)

XML Content:
{content}
"""

VALIDATION_TEST_PROMPT = """
You are a data migration validation expert. Based on the following analyzed {object_type},
generate a structured set of data validation test cases that can be used to compare
results between the legacy Sybase warehouse and the new BigQuery implementation.

The analysis JSON is:
{analysis}

Return ONLY a JSON object with the following structure:
{{
  "object_name": "<table_or_procedure_name>",
  "summary": "High-level description of what should be validated.",
  "metadata": {{
    "type": "table|procedure|mapping",
    "primary_keys": ["pk_col1", ...],
    "tables_read": ["tbl1", ...],
    "tables_modified": ["tbl2", ...]
  }},
  "test_cases": [
    {{
      "name": "Row count comparison",
      "description": "Verify that the total number of rows matches between Sybase and BigQuery.",
      "sql": "SELECT COUNT(*) AS row_count FROM <table>",
      "expected": {{
        "comparison": "equality_between_systems"
      }}
    }},
    {{
      "name": "Aggregate checksum",
      "description": "Example aggregate check across key numeric columns.",
      "sql": "SELECT SUM(<numeric_column>) AS total_value FROM <table>",
      "expected": {{
        "comparison": "equality_between_systems"
      }}
    }}
  ]
}}

Focus on tests such as:
1. Row count comparisons.
2. Aggregate comparisons (SUM, MIN, MAX) on important numeric columns.
3. Distinct count comparisons on key business identifiers.
4. Spot-check filters on important business conditions (e.g. recent dates, statuses).
"""
