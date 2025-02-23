import logging

from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SparkDFExecutionEngine,
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.metrics.column_aggregate_metric_provider import (
    ColumnAggregateMetricProvider,
    column_aggregate_partial,
    column_aggregate_value,
)
from great_expectations.expectations.metrics.import_manager import F, sa

logger = logging.getLogger(__name__)

try:
    from pyspark.sql.functions import stddev_samp  # noqa: F401
except ImportError as e:
    logger.debug(str(e))
    logger.debug(
        "Unable to load spark context; install optional spark dependency for support."
    )


class ColumnStandardDeviation(ColumnAggregateMetricProvider):
    """MetricProvider Class for Aggregate Standard Deviation metric"""

    metric_name = "column.standard_deviation"

    @column_aggregate_value(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        """Pandas Standard Deviation implementation"""
        return column.std()

    @column_aggregate_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(cls, column, _dialect, **kwargs):
        """SqlAlchemy Standard Deviation implementation"""
        if _dialect.name.lower() == "mssql":
            standard_deviation = sa.func.stdev(column)
        else:
            standard_deviation = sa.func.stddev_samp(column)
        return standard_deviation

    @column_aggregate_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column, **kwargs):
        """Spark Standard Deviation implementation"""
        return F.stddev_samp(column)
