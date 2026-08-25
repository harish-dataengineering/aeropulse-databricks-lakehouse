"""
AeroPulse Enterprise Lakehouse Platform.

Reusable functions for pipeline audit logging.
"""

from datetime import datetime, timezone
from typing import Optional
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType


def get_utc_timestamp() -> datetime:
    """
    Return the current UTC timestamp.

    Centralizing timestamp generation makes audit behavior
    consistent across all AeroPulse pipelines.
    """
    return datetime.now(timezone.utc)


def start_pipeline_run(
    spark: SparkSession,
    audit_table: str,
    pipeline_run_id: str,
    pipeline_name: str,
    environment: str,
    layer: Optional[str] = None,
    source_system: Optional[str] = None,
    target_table: Optional[str] = None,
) -> None:
    """
    Create an audit record when a pipeline starts.
    """

    start_timestamp = get_utc_timestamp()

    audit_record = [
        (
            pipeline_run_id,
            pipeline_name,
            environment,
            layer,
            source_system,
            target_table,
            start_timestamp,
            None,
            "RUNNING",
            None,
            None,
            None,
            None,
            None,
            start_timestamp,
        )
    ]

    audit_schema = StructType([
        StructField("pipeline_run_id", StringType(), False),
        StructField("pipeline_name", StringType(), False),
        StructField("environment", StringType(), False),
        StructField("layer", StringType(), True),
        StructField("source_system", StringType(), True),
        StructField("target_table", StringType(), True),
        StructField("start_timestamp", TimestampType(), False),
        StructField("end_timestamp", TimestampType(), True),
        StructField("pipeline_status", StringType(), False),
        StructField("records_read", LongType(), True),
        StructField("records_inserted", LongType(), True),
        StructField("records_updated", LongType(), True),
        StructField("records_rejected", LongType(), True),
        StructField("error_message", StringType(), True),
        StructField("created_timestamp", TimestampType(), False),
    ])

    audit_df = spark.createDataFrame(
        audit_record,
        audit_schema,
    )

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(audit_table)
    )