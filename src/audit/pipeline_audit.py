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


def complete_pipeline_run(
    spark: SparkSession,
    audit_table: str,
    pipeline_run_id: str,
    pipeline_status: str,
    records_read: Optional[int] = None,
    records_inserted: Optional[int] = None,
    records_updated: Optional[int] = None,
    records_rejected: Optional[int] = None,
    error_message: Optional[str] = None,
) -> None:
    """
    Update an audit record when a pipeline completes.
    """

    end_timestamp = get_utc_timestamp()

    from pyspark.sql import functions as F

    # Update the existing audit record for this pipeline run
    audit_df = spark.table(audit_table)
    
    updated_df = (
        audit_df
        .withColumn(
            "end_timestamp",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(end_timestamp)
            ).otherwise(F.col("end_timestamp"))
        )
        .withColumn(
            "pipeline_status",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(pipeline_status)
            ).otherwise(F.col("pipeline_status"))
        )
        .withColumn(
            "records_read",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(records_read)
            ).otherwise(F.col("records_read"))
        )
        .withColumn(
            "records_inserted",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(records_inserted)
            ).otherwise(F.col("records_inserted"))
        )
        .withColumn(
            "records_updated",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(records_updated)
            ).otherwise(F.col("records_updated"))
        )
        .withColumn(
            "records_rejected",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(records_rejected)
            ).otherwise(F.col("records_rejected"))
        )
        .withColumn(
            "error_message",
            F.when(
                F.col("pipeline_run_id") == pipeline_run_id,
                F.lit(error_message)
            ).otherwise(F.col("error_message"))
        )
    )

    (
        updated_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "false")
        .saveAsTable(audit_table)
    )