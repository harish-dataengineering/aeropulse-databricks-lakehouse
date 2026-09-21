# AeroPulse Maintenance Data Quality

## 1. Purpose

The AeroPulse Maintenance Data Quality process validates
Maintenance records after they have been ingested into the
Bronze layer.

The process determines whether Maintenance records are
eligible for downstream trusted processing.

Invalid records are written to the centralized Data Quality
quarantine table.

---

## 2. Source

Source system:

Maintenance Application

Source entity:

Maintenance Events

Source format:

JSON

Ingestion technology:

Databricks Auto Loader

---

## 3. Bronze Table

Development Bronze table:

workspace.aeropulse_dev.bronze_maintenance

Bronze is responsible for preserving ingested source records.

Data Quality does not delete or modify invalid records in
Bronze.

---

## 4. Data Quality Rules

The current Maintenance DQ process contains four rules.

### 4.1 Maintenance Event ID

Rule:

maintenance_event_id must not be NULL.

Rule name:

maintenance_event_id_not_null

---

### 4.2 Aircraft ID

Rule:

aircraft_id must not be NULL.

Rule name:

aircraft_id_not_null

---

### 4.3 Engine ID

Rule:

engine_id must not be NULL.

Rule name:

engine_id_not_null

---

### 4.4 Maintenance Cost

Rule:

maintenance_cost_usd must not be negative.

Rule name:

maintenance_cost_non_negative

---

## 5. Processing Flow

```text
Maintenance Source
        |
        v
Raw Landing
        |
        v
Auto Loader
        |
        v
Bronze Maintenance
        |
        v
Data Quality
      /   \
     /     \
 VALID    INVALID
   |         |
   v         v
Silver   Quarantine
````

---

## 6. Quarantine Table

Development quarantine table:

workspace.aeropulse_dev.dq_quarantine

The quarantine table stores:

* quarantine_id
* quarantine_event_id
* pipeline_run_id
* source_system
* source_entity
* source_file_path
* rule_name
* failure_reason
* record_json
* quarantine_timestamp

---

## 7. Traceability

Each quarantined record contains information that allows
the rejected record to be traced back to its processing
context.

Traceability includes:

* source system
* source entity
* source file
* DQ rule
* failure reason
* pipeline run ID
* original record JSON
* quarantine event ID

---

## 8. Idempotency

Quarantine processing uses a deterministic
quarantine_event_id.

The quarantine write uses Delta MERGE.

The merge condition is:

quarantine_event_id

If the same quarantine event is processed again, an existing
event is not inserted again.

This makes quarantine processing rerun-safe.

---

## 9. Validation Performed

The integration was tested using controlled Maintenance
records containing:

* one valid record
* one record with a NULL aircraft ID
* one record with a NULL engine ID
* one record with a negative maintenance cost

The records were first ingested into Bronze.

The invalid records were then identified by Data Quality and
written to the quarantine table.

The original invalid records remained present in Bronze.

A subsequent rerun of the same DQ execution did not create
duplicate quarantine events.

---

## 10. Design Principle

Bronze preserves source data.

Data Quality determines whether records are trusted for
downstream processing.

Quarantine provides an auditable destination for rejected
records.

Silver will consume the trusted/valid dataset in a later
processing stage.

---

## 11. Current Status

Maintenance Bronze ingestion:

COMPLETED

Maintenance Data Quality:

COMPLETED

Maintenance Quarantine:

COMPLETED

Quarantine Idempotency:

COMPLETED

Maintenance Silver:

NEXT PHASE
