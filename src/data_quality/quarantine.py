"""
AeroPulse Data Quality Quarantine Utility

Purpose
-------
Provides reusable functionality for converting records that
fail data quality validation into the standardized
AeroPulse quarantine format.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def prepare_quarantine_records(
    invalid_df: DataFrame,
    rule_name: str,
    failure_reason: str,
    pipeline_run_id: str,
    source_system: str,
    source_entity: str,
    quarantine_table: str,
) -> DataFrame:
    """
    Convert invalid records into the standardized
    AeroPulse quarantine format.

    The function creates a deterministic quarantine event ID
    so the same rejection event can be identified during
    pipeline reruns.
    """

    # Preserve source file path when available.
    if "_source_file_path" in invalid_df.columns:
        source_file_column = F.col("_source_file_path")
    else:
        source_file_column = F.lit(None).cast("string")

    # Create a deterministic event identifier.
    #
    # We use the pipeline run, source information,
    # rule name, and the complete record as the identity
    # of the rejection event.
    quarantine_event_id = F.sha2(
        F.concat_ws(
            "||",
            F.lit(pipeline_run_id),
            F.lit(source_system),
            F.lit(source_entity),
            F.lit(rule_name),
            F.to_json(
                F.struct(
                    *[
                        F.col(column)
                        for column in invalid_df.columns
                    ]
                )
            ),
        ),
        256,
    )

    return (
        invalid_df
        .withColumn(
            "quarantine_id",
            F.expr("uuid()")
        )
        .withColumn(
            "quarantine_event_id",
            quarantine_event_id
        )
        .withColumn(
            "pipeline_run_id",
            F.lit(pipeline_run_id)
        )
        .withColumn(
            "source_system",
            F.lit(source_system)
        )
        .withColumn(
            "source_entity",
            F.lit(source_entity)
        )
        .withColumn(
            "source_file_path",
            source_file_column
        )
        .withColumn(
            "rule_name",
            F.lit(rule_name)
        )
        .withColumn(
            "failure_reason",
            F.lit(failure_reason)
        )
        .withColumn(
            "record_json",
            F.to_json(
                F.struct(
                    *[
                        F.col(column)
                        for column in invalid_df.columns
                    ]
                )
            )
        )
        .withColumn(
            "quarantine_timestamp",
            F.current_timestamp()
        )
        .select(
            "quarantine_id",
            "quarantine_event_id",
            "pipeline_run_id",
            "source_system",
            "source_entity",
            "source_file_path",
            "rule_name",
            "failure_reason",
            "record_json",
            "quarantine_timestamp",
        )
    )