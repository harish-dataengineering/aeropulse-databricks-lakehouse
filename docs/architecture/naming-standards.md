# AeroPulse Naming Standards

## 1. Purpose

This document defines the naming standards for the AeroPulse Enterprise Lakehouse Platform.

The objective is to ensure consistency, readability, maintainability, and predictable naming across Databricks data objects, source code, pipelines, configuration files, and documentation.

---

# 2. General Naming Principles

All names should follow these principles:

1. Use lowercase characters.
2. Use snake_case for multi-word names.
3. Avoid spaces.
4. Avoid special characters.
5. Use descriptive names.
6. Avoid unnecessary abbreviations.
7. Avoid environment-specific hardcoding in source code.
8. Use consistent prefixes for related objects.
9. Do not use temporary or personal names for production objects.

---

# 3. Databricks Naming Standards

## 3.1 Catalog

The initial project will use the existing Unity Catalog catalog:

```text
workspace
```

---

## 3.2 Environment Schemas

The project environments will be represented using the following schemas:

```text
workspace.aeropulse_dev
workspace.aeropulse_test
workspace.aeropulse_prod
```

Environment naming:

| Environment | Schema         |
| ----------- | -------------- |
| Development | aeropulse_dev  |
| Testing     | aeropulse_test |
| Production  | aeropulse_prod |

---

## 3.3 Table Naming

Tables will use descriptive names.

Examples:

```text
bronze_engine_telemetry
silver_engine_telemetry
gold_engine_health_daily
audit_pipeline_runs
audit_data_quality_results
```

The naming convention is:

```text
<layer_or_domain>_<business_entity>_<optional_purpose>
```

---

# 4. Medallion Layer Naming

## Bronze

```text
bronze_<entity_name>
```

Examples:

```text
bronze_aircraft
bronze_engines
bronze_flights
bronze_engine_telemetry
```

---

## Silver

```text
silver_<entity_name>
```

Examples:

```text
silver_aircraft
silver_engines
silver_flights
silver_engine_telemetry
```

---

## Gold

```text
gold_<business_purpose>
```

Examples:

```text
gold_engine_health_daily
gold_maintenance_kpis
gold_supplier_performance
gold_inventory_summary
```

Gold tables must represent business-ready datasets and should not be created automatically for every Silver table.

---

# 5. Audit and Monitoring Tables

Audit tables will use the following prefix:

```text
audit_
```

Examples:

```text
audit_pipeline_runs
audit_data_quality_results
audit_errors
audit_ingestion_metrics
```

---

# 6. Column Naming

All columns must use lowercase snake_case.

Examples:

```text
engine_id
flight_id
source_system
source_file_name
ingestion_timestamp
created_timestamp
updated_timestamp
record_status
```

Timestamp columns should end with:

```text
_timestamp
```

Date columns should end with:

```text
_date
```

Identifier columns should generally end with:

```text
_id
```

Boolean columns should use clear descriptive names such as:

```text
is_active
is_deleted
is_valid
has_failed
```

---

# 7. Standard Metadata Columns

Where appropriate, Bronze and Silver tables will include metadata columns.

Examples:

```text
source_system
source_file_name
ingestion_timestamp
pipeline_run_id
record_hash
```

The exact metadata columns may vary depending on the source and ingestion pattern.

---

# 8. Python Naming Standards

Python files will use lowercase snake_case.

Examples:

```text
audit_logger.py
data_quality.py
bronze_ingestion.py
telemetry_processor.py
```

Functions:

```python
read_source_data()
write_audit_record()
validate_dataframe()
process_engine_telemetry()
```

Variables:

```python
source_df
target_table
pipeline_run_id
record_count
```

Classes will use PascalCase only when object-oriented design provides a clear benefit.

Examples:

```python
AuditLogger
ApiClient
PipelineConfig
```

Object-oriented programming will not be used unnecessarily.

---

# 9. Pipeline and Job Naming

Pipeline and job names will follow:

```text
<environment>_<layer>_<domain>_<purpose>
```

Examples:

```text
dev_bronze_fleet_ingestion
dev_bronze_telemetry_ingestion
dev_silver_engine_processing
dev_gold_engine_health
```

---

# 10. Source System Naming

Source systems will use standardized identifiers:

```text
erp
fleet_ops
flight_ops
iot_telemetry
supply_chain
manufacturing
external_api
```

Example:

```text
source_system = "iot_telemetry"
```

---

# 11. Configuration File Naming

Environment configuration files:

```text
configs/dev.yml
configs/test.yml
configs/prod.yml
```

Future shared configuration:

```text
configs/project.yml
configs/source_systems.yml
configs/data_quality_rules.yml
```

---

# 12. Git Branch Naming

Branches will follow:

```text
feature/<feature_name>
bugfix/<issue_name>
hotfix/<issue_name>
release/<version>
```

Examples:

```text
feature/project-foundation
feature/bronze-ingestion
feature/telemetry-streaming
bugfix/telemetry-duplicate-handling
```

The `main` branch will represent the stable version of the project.

---

# 13. Naming Anti-Patterns

The following names are not acceptable:

```text
test
test1
test_final
test_final_v2
new_table
table_latest
harish_table
temp
tmp_data
data123
```

Names must clearly communicate the purpose of the object.
