"""
AeroPulse Data Quality Framework

Purpose
-------
Provides reusable data quality validation utilities
for AeroPulse ingestion and transformation pipelines.

Responsibilities
----------------
1. Execute configurable data quality rules.
2. Capture rule-level results.
3. Identify valid and invalid records.
4. Produce standardized validation results.
5. Support Bronze-to-Silver data quality gates.

Design
------
The framework is intentionally source-agnostic.

Business pipelines define the rules.
The framework executes and standardizes them.
"""


from dataclasses import dataclass
from typing import Callable, List

from pyspark.sql import DataFrame

@dataclass
class DataQualityRule:
    rule_name: str
    description: str
    check_function: Callable[[DataFrame], DataFrame]


def run_data_quality_rule(
    df: DataFrame,
    rule: DataQualityRule
) -> dict:
    """
    Execute one data quality rule and return
    a standardized result.
    """

    invalid_df = rule.check_function(df)

    invalid_count = invalid_df.count()

    total_count = df.count()

    passed = invalid_count == 0

    return {
        "rule_name": rule.rule_name,
        "description": rule.description,
        "total_records": total_count,
        "invalid_records": invalid_count,
        "passed": passed,
    }


def null_check(
    column_name: str
) -> Callable[[DataFrame], DataFrame]:

    def check(df: DataFrame) -> DataFrame:
        return df.filter(
            df[column_name].isNull()
        )

    return check


def duplicate_check(
    column_name: str
) -> Callable[[DataFrame], DataFrame]:

    def check(df: DataFrame) -> DataFrame:

        duplicate_keys = (
            df.groupBy(column_name)
            .count()
            .filter("count > 1")
            .select(column_name)
        )

        return df.join(
            duplicate_keys,
            on=column_name,
            how="inner"
        )

    return check
