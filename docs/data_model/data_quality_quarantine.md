# AeroPulse Data Quality and Quarantine Architecture

## 1. Purpose

The AeroPulse Data Quality and Quarantine framework identifies records
that fail defined data quality rules and stores those rejected records
in a centralized Delta Lake quarantine table.

The framework is designed to support:

- reusable data quality rules
- record-level rejection
- centralized quarantine
- pipeline auditability
- deterministic quarantine event identification
- idempotent pipeline retries
- multiple data quality rules
- separation of valid and invalid records

---

## 2. Architecture

The framework follows this flow:

Source Data
    |
    v
Data Quality Rule
    |
    +--------------------+
    |                    |
    v                    v
Valid Records       Invalid Records
    |                    |
    v                    v
Continue Pipeline   Prepare Quarantine
                         |
                         v
                  Deterministic Event ID
                         |
                         v
                    Delta MERGE
                         |
                         v
                Central Quarantine Table

---

## 3. Data Quality Framework

The Data Quality framework provides reusable rule definitions.

A rule contains:

- rule name
- description
- validation function

Example rules include:

- NOT NULL validation
- duplicate detection

The framework separates rule definition from rule execution.

---

## 4. Quarantine Framework

The quarantine utility converts invalid records into a standardized
quarantine structure.

Each quarantine event contains:

- quarantine_id
- quarantine_event_id
- pipeline_run_id
- source_system
- source_entity
- source_file_path
- rule_name
- failure_reason
- record_json
- quarantine_timestamp

---

## 5. Deterministic Quarantine Event ID

A deterministic SHA-256 hash is generated from the pipeline execution
context and rejected record.

This allows the same rejection event to be recognized during pipeline
retries.

The quarantine writer uses the event ID as the MERGE key.

---

## 6. Idempotency

Quarantine writes use Delta MERGE rather than unconditional append.

If the same quarantine event already exists:

- the existing event is retained
- a duplicate event is not inserted

This makes quarantine writes safe during pipeline retries.

---

## 7. Multiple Data Quality Rules

Multiple rules can be executed against the same DataFrame.

Each rule produces its own rejection events.

For example:

- aircraft_id_not_null
- maintenance_id_unique

A single pipeline execution can therefore produce multiple quarantine
events for different rule failures.

---

## 8. Valid Records

Records that pass a rule are not written to quarantine.

The reusable validation function returns:

- rule name
- invalid record count
- whether records were quarantined

This allows downstream pipeline logic to distinguish successful validation
from rejected records.

---

## 9. Reusable Orchestration

The `validate_and_quarantine()` function provides a reusable interface
for executing the complete validation and quarantine process.

It internally performs:

1. DQ rule execution
2. invalid-record detection
3. quarantine record preparation
4. idempotent quarantine write

This keeps production notebooks simpler and moves reusable logic into
the shared framework.

---

## 10. Testing Performed

The framework has been tested for:

- single DQ rule failures
- multiple DQ rule failures
- valid records
- invalid records
- duplicate quarantine prevention
- repeated pipeline execution
- multiple legitimate pipeline runs
- end-to-end DQ-to-quarantine processing

---

## 11. AeroPulse Design Principle

The quarantine table is an audit and recovery mechanism.

Rejected records are preserved rather than silently discarded.

This allows future processes to:

- investigate data quality failures
- identify problematic source deliveries
- measure recurring quality issues
- correct source data
- replay corrected records