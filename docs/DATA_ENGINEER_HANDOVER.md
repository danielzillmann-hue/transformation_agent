# Transformation Agent - Data Engineer Handover Guide

## Overview

The **Transformation Agent** is an AI-powered tool that automates the migration of legacy ETL pipelines from **multiple source database systems** to **Google Cloud Platform (BigQuery/Dataform)**. It analyzes source schemas, stored procedures, and ETL mappings, then generates equivalent Dataform SQLX files ready for deployment.

### Supported Source Systems

| Source Database | ETL Tool Support |
|-----------------|------------------|
| Sybase ASE | Informatica PowerCenter |
| Oracle | ODI, Informatica |
| SQL Server | SSIS, Informatica |
| MySQL / MariaDB | Pentaho, Informatica |
| PostgreSQL | dbt, Informatica |
| Teradata | Informatica, BTEQ |
| Snowflake | dbt |

---

## Table of Contents

1. [Architecture](#architecture)
2. [Pipeline Stages](#pipeline-stages)
3. [Source System Configuration](#source-system-configuration)
4. [Input Requirements](#input-requirements)
5. [Output Artifacts](#output-artifacts)
6. [Running the Pipeline](#running-the-pipeline)
7. [Configuration Options](#configuration-options)
8. [Generated Dataform Project Structure](#generated-dataform-project-structure)
9. [SCD Type Detection](#scd-type-detection)
10. [Informatica Mapping Conversion](#informatica-mapping-conversion)
11. [Validation Tests](#validation-tests)
12. [Troubleshooting](#troubleshooting)
13. [Post-Migration Steps](#post-migration-steps)

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
- **Source Adapters** - Configurable per-database type mappings and prompts

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
- Converts source DDL to BigQuery Dataform SQLX
- Uses source-specific type mappings from adapter config
- Detects SCD Type 1 vs Type 2 tables
- Generates incremental loading patterns for fact tables
- Converts Informatica mappings to transformation SQL with function mapping hints

### 5. Validation
- Generates test case definitions for data quality
- Creates human-readable validation report
- **Parallelized**: 5 concurrent LLM calls

---

## Source System Configuration

The tool uses YAML configuration files to define source-specific settings for each database system.

### Config File Location

```
config/source_systems/
├── _template.yaml    # Template for creating custom configs
├── sybase.yaml       # Sybase ASE (default)
├── oracle.yaml       # Oracle Database
├── sqlserver.yaml    # SQL Server / Azure SQL
├── mysql.yaml        # MySQL / MariaDB
├── postgres.yaml     # PostgreSQL
├── teradata.yaml     # Teradata
└── snowflake.yaml    # Snowflake
```

### What Each Config Contains

| Section | Description |
|---------|-------------|
| `type_mappings` | Source → BigQuery data type conversions |
| `file_patterns` | How to detect DDL, procedures, ETL files |
| `table_classification` | Dimension/fact/staging prefixes |
| `scd_detection` | Type 1 and Type 2 table lists, column indicators |
| `incremental_patterns` | Regex patterns for incremental tables |
| `domain_mapping` | Business domain → BigQuery dataset mapping |
| `function_mappings` | Source SQL functions → BigQuery equivalents |
| `prompts` | Custom LLM prompts for analysis |

### Creating a Custom Config

1. Copy `_template.yaml` to a new file (e.g., `my_database.yaml`)
2. Fill in the required sections:
   ```yaml
   name: "My Custom Database"
   
   type_mappings:
     INT: INT64
     VARCHAR: STRING
     DATETIME: TIMESTAMP
     # Add your type mappings...
   
   file_patterns:
     ddl:
       extensions: [".sql", ".ddl"]
   ```
3. Save the file - it will automatically appear in the UI dropdown

### Example: Oracle Type Mappings

```yaml
# From config/source_systems/oracle.yaml
type_mappings:
  NUMBER: NUMERIC
  VARCHAR2: STRING
  CLOB: STRING
  DATE: TIMESTAMP        # Oracle DATE includes time
  RAW: BYTES
  BLOB: BYTES
  ROWID: STRING
  XMLTYPE: STRING
```

### Example: Function Mappings for SQL Conversion

```yaml
# From config/source_systems/oracle.yaml
oracle_specific:
  function_mappings:
    NVL: IFNULL
    NVL2: "IF(condition, value_if_not_null, value_if_null)"
    DECODE: CASE
    SYSDATE: CURRENT_TIMESTAMP
    TO_DATE: PARSE_TIMESTAMP
    TO_CHAR: FORMAT_TIMESTAMP
    TRUNC: DATE_TRUNC
    ADD_MONTHS: DATE_ADD
    MONTHS_BETWEEN: DATE_DIFF
    ROWNUM: ROW_NUMBER
    LISTAGG: STRING_AGG
```

These function mappings are passed to the LLM when converting Informatica mappings, helping it produce accurate BigQuery SQL.

---

## Input Requirements

### Supported File Types

| File Type | Extension | Description |
|-----------|-----------|-------------|
| DDL Scripts | `.sql`, `.ddl` | CREATE TABLE, ALTER TABLE statements |
| Stored Procedures | `.sql`, `.prc`, `.pkg` | Database-specific procedures |
| Informatica Mappings | `.XML` | PowerCenter mapping exports |
| SSIS Packages | `.dtsx` | SQL Server Integration Services (future) |
| dbt Models | `.sql`, `.yml` | dbt model definitions (future) |

### GCS Bucket Structure

```
gs://your-bucket/
├── D_*.sql          # Dimension table DDL
├── F_*.sql          # Fact table DDL
├── m_*.XML          # Informatica mapping exports
└── *.sql            # Other DDL/procedures
```

### Naming Conventions

The tool uses naming conventions (configurable per source system) to classify files:
- `D_*` or `dim_*` → Dimension tables
- `F_*` or `fact_*` → Fact tables
- `m_*.XML` → Informatica mappings
- `wkf_*.XML` → Informatica workflows (skipped)

These patterns are defined in each source system's YAML config under `table_classification`.

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
2. **Select Source Database System** from dropdown (Sybase, Oracle, SQL Server, etc.)
3. Select source GCS bucket and archive bucket
4. Configure options (validation, project ID)
5. Click "Start Migration"
6. Monitor progress via SSE updates

### Command Line

```bash
python main.py \
  --source-system oracle \
  --bucket your-source-bucket \
  --project dan-sandpit \
  --output ./output
```

### Available Source Systems

```bash
# List available source systems
python -c "from src.adapters.registry import get_registry; print(get_registry().list_available())"
# Output: ['mysql', 'oracle', 'postgres', 'snowflake', 'sqlserver', 'sybase', 'teradata']
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

### Source System Selection

The source system determines:
- Data type mappings
- File detection patterns
- SCD detection rules
- Function mappings for SQL conversion
- Custom LLM prompts

### Custom Type Mappings (Runtime Override)

For runtime overrides without editing YAML configs, create `gs://your-bucket/config/type_mappings.txt`:
```
# Source type -> BigQuery type
MONEY=NUMERIC(19,4)
SMALLMONEY=NUMERIC(10,4)
IMAGE=BYTES
```

### Type Mappings by Source System

**Sybase ASE:**
| Source Type | BigQuery Type |
|-------------|---------------|
| INT, INTEGER, SMALLINT, TINYINT, BIGINT | INT64 |
| DECIMAL, NUMERIC | NUMERIC |
| MONEY | NUMERIC(19,4) |
| CHAR, VARCHAR, TEXT | STRING |
| DATETIME | TIMESTAMP |
| BIT | BOOL |

**Oracle:**
| Source Type | BigQuery Type |
|-------------|---------------|
| NUMBER | NUMERIC |
| VARCHAR2, CLOB | STRING |
| DATE | TIMESTAMP |
| RAW, BLOB | BYTES |
| ROWID | STRING |

**SQL Server:**
| Source Type | BigQuery Type |
|-------------|---------------|
| INT, BIGINT, SMALLINT | INT64 |
| DECIMAL, MONEY | NUMERIC |
| VARCHAR, NVARCHAR, TEXT | STRING |
| DATETIME, DATETIME2 | TIMESTAMP |
| UNIQUEIDENTIFIER | STRING |
| BIT | BOOL |

See `config/source_systems/*.yaml` for complete mappings.

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
  - **Source-specific function conversions** (e.g., Oracle `NVL` → BigQuery `IFNULL`)

### Source-Aware SQL Conversion

The Informatica converter uses the selected source system's function mappings to help the LLM produce accurate BigQuery SQL. For example, when converting an Oracle-based mapping:

```
**Source Database**: Oracle

**Function Mappings** (used for conversion):
{
  "NVL": "IFNULL",
  "DECODE": "CASE",
  "SYSDATE": "CURRENT_TIMESTAMP",
  "TO_DATE": "PARSE_TIMESTAMP",
  "SUBSTR": "SUBSTRING",
  "INSTR": "STRPOS"
}
```

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

-- Note: Oracle functions converted to BigQuery equivalents
WITH source_data AS (
  SELECT 
    IFNULL(d.dept_name, 'Unknown') as dept_name,  -- Was: NVL(d.dept_name, 'Unknown')
    PARSE_TIMESTAMP('%Y-%m-%d', p.promo_date) as promo_date,  -- Was: TO_DATE(p.promo_date, 'YYYY-MM-DD')
    ...
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
4. Check source system config in `config/source_systems/` for type mapping issues

---

## Appendix A: Adding a New Source System

### Step 1: Create Config File

```bash
cp config/source_systems/_template.yaml config/source_systems/my_database.yaml
```

### Step 2: Define Type Mappings

```yaml
name: "My Database"
description: "My Database to BigQuery migration"

type_mappings:
  INT: INT64
  VARCHAR: STRING
  TIMESTAMP: TIMESTAMP
  # Add all your database's types...
```

### Step 3: Define File Patterns

```yaml
file_patterns:
  ddl:
    extensions: [".sql", ".ddl"]
    prefixes: ["D_", "F_"]  # Optional
  procedures:
    extensions: [".sql", ".prc"]
    prefixes: ["sp_", "usp_"]
  etl_exports:
    extensions: [".xml"]
    tool: "informatica"  # or "ssis", "odi", "dbt"
```

### Step 4: Define SCD Rules

```yaml
scd_detection:
  type2_tables:
    - customer
    - employee
  type1_tables:
    - status
    - type
    - date
  type2_column_indicators:
    - effective_date
    - valid_from
    - is_current
```

### Step 5: Add Function Mappings (Optional)

```yaml
function_mappings:
  MY_FUNC: BQ_EQUIVALENT
  CUSTOM_DATE: DATE_TRUNC
```

### Step 6: Test

The new config will automatically appear in the UI dropdown and CLI options.

---

## Appendix B: Dependency Graph

The tool generates a Mermaid diagram (`dependency_graph.mmd`) showing:
- **Tables** (blue) - Dimension and fact tables
- **Procedures** (yellow) - Stored procedures
- **Mappings** (purple) - Informatica ETL mappings
- **Edges** - FK relationships, source/target connections

View in any Mermaid-compatible viewer or paste into:
- GitHub markdown
- Confluence
- https://mermaid.live

---

## Appendix C: Cloud Run Deployment Notes

### Config Files in Docker

The source system configs are bundled into the Docker image at build time:

```dockerfile
COPY config/ /app/config/
```

### Customizing Configs for Deployment

**Option 1: Edit before building**
```bash
# Edit config files locally
vim config/source_systems/sybase.yaml

# Rebuild and deploy
gcloud builds submit --tag gcr.io/PROJECT/transformation-agent
gcloud run deploy ...
```

**Option 2: Mount from GCS (requires code change)**
```python
# In registry.py, add GCS config loading
AdapterRegistry.set_config_dir("gs://my-bucket/configs/")
```

### Environment Variables for Cloud Run

```bash
gcloud run deploy transformation-agent \
  --set-env-vars="ANALYSIS_MAX_WORKERS=10,VALIDATION_MAX_WORKERS=10"
```
