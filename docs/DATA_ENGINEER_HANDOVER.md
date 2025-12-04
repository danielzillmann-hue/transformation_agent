# Transformation Agent - Data Engineer Handover Guide

## Overview

The **Transformation Agent** is an AI-powered tool that automates the migration of legacy ETL pipelines from **Sybase/Informatica** to **Google Cloud Platform (BigQuery/Dataform)**. It analyzes source schemas, stored procedures, and Informatica mappings, then generates equivalent Dataform SQLX files ready for deployment.

---

## Table of Contents

1. [Architecture](#architecture)
2. [Pipeline Stages](#pipeline-stages)
3. [Input Requirements](#input-requirements)
4. [Output Artifacts](#output-artifacts)
5. [Running the Pipeline](#running-the-pipeline)
6. [Configuration Options](#configuration-options)
7. [Generated Dataform Project Structure](#generated-dataform-project-structure)
8. [SCD Type Detection](#scd-type-detection)
9. [Informatica Mapping Conversion](#informatica-mapping-conversion)
10. [Validation Tests](#validation-tests)
11. [Troubleshooting](#troubleshooting)
12. [Post-Migration Steps](#post-migration-steps)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Transformation Agent                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐   ┌──────────┐   ┌─────────────┐   ┌────────────┐   ┌──────┐ │
│  │ Ingestion│ → │ Analysis │ → │Categorization│ → │ Translation│ → │Output│ │
│  │  Engine  │   │  Engine  │   │   Engine    │   │   Engine   │   │      │ │
│  └──────────┘   └──────────┘   └─────────────┘   └────────────┘   └──────┘ │
│       ↑              ↑               ↑                ↑              ↓      │
│       │              │               │                │              │      │
│  ┌────┴────┐    ┌────┴────┐    ┌─────┴─────┐   ┌─────┴─────┐   ┌────┴────┐ │
│  │  GCS    │    │  LLM    │    │   LLM     │   │   LLM     │   │  GCS    │ │
│  │ Bucket  │    │(Gemini) │    │ (Gemini)  │   │ (Gemini)  │   │ Archive │ │
│  └─────────┘    └─────────┘    └───────────┘   └───────────┘   └─────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Vertex AI (Gemini 2.5 Flash)** - LLM for schema analysis and code generation
- **Google Cloud Storage** - Input/output file storage
- **FastAPI** - Web interface for running migrations
- **Dataform** - Target transformation framework

---

## Pipeline Stages

### 1. Ingestion
- Reads files from GCS bucket or local directory
- Supports: `.sql` (DDL/procedures), `.XML` (Informatica exports)

### 2. Analysis
- Uses LLM to extract structured metadata from each file
- Identifies: table names, columns, data types, foreign keys, stored procedure logic
- **Parallelized**: 5 concurrent LLM calls (configurable)

### 3. Categorization
- Infers business domains from table schemas
- Maps tables to target BigQuery datasets
- **Batched**: 8 tables per LLM call for efficiency

### 4. Translation
- Converts Sybase DDL to BigQuery Dataform SQLX
- Detects SCD Type 1 vs Type 2 tables
- Generates incremental loading patterns for fact tables
- Converts Informatica mappings to transformation SQL

### 5. Validation
- Generates test case definitions for data quality
- Creates human-readable validation report
- **Parallelized**: 5 concurrent LLM calls

---

## Input Requirements

### Supported File Types

| File Type | Extension | Description |
|-----------|-----------|-------------|
| Sybase DDL | `.sql` | CREATE TABLE, ALTER TABLE statements |
| Stored Procedures | `.sql` | Sybase stored procedures (prefixed with naming convention) |
| Informatica Mappings | `.XML` | PowerCenter mapping exports |

### GCS Bucket Structure

```
gs://your-bucket/
├── D_*.sql          # Dimension table DDL
├── F_*.sql          # Fact table DDL
├── m_*.XML          # Informatica mapping exports
└── *.sql            # Other DDL/procedures
```

### Naming Conventions

The tool uses naming conventions to classify files:
- `D_*` or `dim_*` → Dimension tables
- `F_*` or `fact_*` → Fact tables
- `m_*.XML` → Informatica mappings
- `wkf_*.XML` → Informatica workflows (skipped)

---

## Output Artifacts

### Generated Files

| File | Description |
|------|-------------|
| `analysis_results.json` | Raw LLM analysis for each input file |
| `analysis_report.txt` | Human-readable analysis summary |
| `data_categorization.json` | Domain/dataset mappings |
| `dependency_graph.mmd` | Mermaid diagram of table relationships |
| `validation_tests.json` | Generated test case definitions |
| `validation_report.txt` | Human-readable test documentation |
| `informatica_shared_objects.md` | Reference doc for reusable Informatica components |
| `dataform/` | Complete Dataform project (see below) |

### GCS Archive

All outputs are archived to:
```
gs://your-archive-bucket/migration_YYYYMMDD_HHMMSS/
```

---

## Running the Pipeline

### Web Interface

1. Navigate to the deployed Cloud Run URL
2. Select source GCS bucket and archive bucket
3. Configure options (validation, project ID)
4. Click "Start Migration"
5. Monitor progress via SSE updates

### Command Line

```bash
python main.py \
  --bucket your-source-bucket \
  --project dan-sandpit \
  --output ./output
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANALYSIS_MAX_WORKERS` | 5 | Parallel LLM calls for analysis |
| `VALIDATION_MAX_WORKERS` | 5 | Parallel LLM calls for validation |
| `SCD_DETECTION_USE_LLM` | true | Enable LLM-based SCD type detection |
| `TYPE_MAPPING_BUCKET` | - | GCS bucket for custom type mappings |
| `TYPE_MAPPING_PATH` | config/type_mappings.txt | Path to type mapping overrides |

---

## Configuration Options

### Custom Type Mappings

Create `gs://your-bucket/config/type_mappings.txt`:
```
# Sybase type -> BigQuery type
MONEY=NUMERIC(19,4)
SMALLMONEY=NUMERIC(10,4)
IMAGE=BYTES
```

### Default Type Mappings

| Sybase Type | BigQuery Type |
|-------------|---------------|
| INT, INTEGER, SMALLINT, TINYINT, BIGINT | INT64 |
| DECIMAL, NUMERIC | NUMERIC |
| MONEY | NUMERIC(19,4) |
| FLOAT, REAL | FLOAT64 |
| CHAR, VARCHAR, TEXT, NCHAR, NVARCHAR | STRING |
| DATETIME, SMALLDATETIME | TIMESTAMP |
| DATE | DATE |
| TIME | TIME |
| BIT | BOOL |
| BINARY, VARBINARY, IMAGE | BYTES |

---

## Generated Dataform Project Structure

```
output/dataform/
├── dataform.json                    # Project configuration
├── definitions/
│   ├── crown_customer_loyalty/      # Customer domain tables
│   │   ├── d_patron.sqlx
│   │   └── d_member.sqlx
│   ├── crown_gaming_activity/       # Gaming activity tables
│   │   ├── f_gamingrating.sqlx
│   │   └── f_promotion_transaction.sqlx
│   ├── crown_reference/             # Reference/lookup tables
│   │   ├── d_age.sqlx
│   │   └── d_status_code.sqlx
│   ├── intermediate/                # Informatica transformation conversions
│   │   └── m_promotion_transaction.sqlx
│   └── staging/                     # Staging tables (if needed)
└── includes/                        # Shared SQL functions
```

### Domain to Dataset Mapping

| Business Domain | BigQuery Dataset |
|-----------------|------------------|
| Customer & Loyalty Management | crown_customer_loyalty |
| Casino Operations & Locations | crown_casino_operations |
| Gaming Products & Assets | crown_gaming_products |
| Gaming Activity & Performance | crown_gaming_activity |
| Promotions & Marketing | crown_promotions |
| Regulatory & Compliance | crown_regulatory |
| Reference & Time Data | crown_reference |

---

## SCD Type Detection

The tool automatically detects whether dimension tables should use **SCD Type 1** (overwrite) or **SCD Type 2** (history tracking).

### Detection Logic (Priority Order)

1. **Explicit Type 1 Override** - Reference tables that should never track history:
   - Age, Site, Location, Product, Machine, Department, License, Date/Time dimensions

2. **Explicit Type 2 List** - Tables representing people:
   - Patron, Customer, Member, Employee

3. **Heuristic Detection** - Column patterns:
   - Type 2 indicators: `effective_date`, `expiry_date`, `is_current`, `version`
   - Type 1 indicators: `code`, `description` only (simple lookups)

4. **LLM Detection** (optional) - Schema analysis for ambiguous cases

### Generated SQLX Patterns

**SCD Type 1 (Full Replace):**
```sql
config {
  type: "table",
  schema: "crown_reference",
  description: "Dimension table: D_AGE (SCD Type 1 - Full Replace)"
}

SELECT
  AGE_KEY,
  AGE_DESC,
  CURRENT_TIMESTAMP() as _loaded_at
FROM ${ref('source_table')}
```

**SCD Type 2 (History Tracking):**
```sql
config {
  type: "incremental",
  schema: "crown_customer_loyalty",
  uniqueKey: ["PATRON_KEY", "_valid_from"],
  description: "Dimension table: D_PATRON (SCD Type 2 - History Tracking)"
}

-- Includes merge logic for tracking changes with valid_from/valid_to dates
```

---

## Informatica Mapping Conversion

### What Gets Converted

- **Complete mappings** (`m_*.XML`) with sources, targets, and transformation logic
- Generates Dataform SQLX with:
  - Source table references using `${ref('table_name')}`
  - Transformation logic as CTEs
  - Target table configuration

### What Gets Documented (Not Converted)

- **Shared/Reusable objects** - Lookups, expressions, aggregators stored in folders
- These are documented in `informatica_shared_objects.md` for reference

### Example Converted Mapping

**Input:** `m_Promotion_Transaction.XML`

**Output:** `intermediate/m_promotion_transaction.sqlx`
```sql
-- Dataform transformation from Informatica mapping
-- Mapping: m_Promotion_Transaction
-- Sources: D_Department, D_Promotion_Details, D_CASINOLOCATIONDET, D_HOUR
-- Targets: F_Promotion_Transaction

config {
  type: "view",
  schema: "crown_promotions",
  description: "Informatica mapping: m_Promotion_Transaction",
  dependencies: ["D_Department", "D_Promotion_Details", "D_CASINOLOCATIONDET"]
}

WITH source_data AS (
  SELECT ...
  FROM ${ref('D_Department')} d
  JOIN ${ref('D_Promotion_Details')} p ON ...
)
SELECT * FROM source_data
```

---

## Validation Tests

### Generated Test Types

1. **Row Count Tests** - Verify expected record counts
2. **Null Checks** - Validate required columns
3. **Referential Integrity** - Check foreign key relationships
4. **Data Type Validation** - Ensure correct formats
5. **Business Rule Tests** - Domain-specific validations

### Output Files

- `validation_tests.json` - Machine-readable test definitions
- `validation_report.txt` - Human-readable documentation

### Example Test Case

```json
{
  "name": "FK_D_PATRON_exists",
  "description": "Verify all PATRON_KEY values exist in D_PATRON",
  "sql": "SELECT COUNT(*) FROM F_GAMINGRATING f LEFT JOIN D_PATRON p ON f.PATRON_KEY = p.PATRON_KEY WHERE p.PATRON_KEY IS NULL",
  "expected": {"count": 0}
}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `403 Permission denied` | Wrong GCP project | Set correct project ID in config |
| `UnicodeDecodeError` | Non-UTF-8 files | Automatic fallback to latin-1 encoding |
| `JSON parsing error` | Malformed LLM response | Uses `safe_parse_json` with repair |
| `504 Gateway Timeout` | Pipeline too slow | Parallelization reduces runtime |
| Missing Mermaid chart | File not uploaded | Now included in GCS archive |

### Log Messages

| Log Level | Example | Meaning |
|-----------|---------|---------|
| INFO | `Analyzing file 5/20: D_PATRON.sql` | Normal progress |
| WARNING | `Skipping file - no mapping name found` | Shared object (expected) |
| ERROR | `Failed to read file: encoding error` | Check file encoding |

### Performance Tuning

For large migrations (100+ files):
```bash
export ANALYSIS_MAX_WORKERS=10
export VALIDATION_MAX_WORKERS=10
```

---

## Post-Migration Steps

### 1. Review Generated SQLX

- Verify column mappings are correct
- Check SCD type assignments
- Review transformation logic from Informatica conversions

### 2. Deploy to Dataform

```bash
cd output/dataform
dataform init  # If not already initialized
dataform compile
dataform run
```

### 3. Run Validation Tests

Use the generated `validation_tests.json` to create Dataform assertions or BigQuery scheduled queries.

### 4. Update Dependencies

Review `dependency_graph.mmd` to understand table relationships and ensure correct execution order.

### 5. Configure Incremental Loads

For fact tables, configure:
- Partition columns (usually date-based)
- Clustering keys
- Incremental predicates

---

## Support

For issues or questions:
1. Check Cloud Run logs for detailed error messages
2. Review `analysis_results.json` for LLM interpretation issues
3. Consult `informatica_shared_objects.md` for undocumented components

---

## Appendix: Dependency Graph

The tool generates a Mermaid diagram (`dependency_graph.mmd`) showing:
- **Tables** (blue) - Dimension and fact tables
- **Procedures** (yellow) - Stored procedures
- **Mappings** (purple) - Informatica ETL mappings
- **Edges** - FK relationships, source/target connections

View in any Mermaid-compatible viewer or paste into:
- GitHub markdown
- Confluence
- https://mermaid.live
