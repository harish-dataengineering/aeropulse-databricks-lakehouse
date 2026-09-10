"""
AeroPulse Data Quality Quarantine Utility

Purpose
-------
Provides reusable functionality for writing records that
fail data quality validation into the centralized
quarantine Delta table.
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

    Parameters
    ----------
    invalid_df : DataFrame
        Records that failed a data quality rule.

    rule_name : str
        Name of the failed data quality rule.

    failure_reason : str
        Human-readable explanation of the failure.

    pipeline_run_id : str
        Identifier for the pipeline execution.

    source_system : str
        Name of the originating source system.

    source_entity : str
        Business entity represented by the records.

    quarantine_table : str
        Fully qualified quarantine table name.

    Returns
    -------
    DataFrame
        DataFrame formatted for the centralized
        AeroPulse quarantine table.
    """

    # Preserve source file path when available.
    # This allows us to trace an invalid record
    # back to the physical source delivery.
    if "_source_file_path" in invalid_df.columns:
        source_file_column = F.col("_source_file_path")
    else:
        source_file_column = F.lit(None).cast("string")

    return (
        invalid_df
        .withColumn(
            "quarantine_id",
            F.expr("uuid()")
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