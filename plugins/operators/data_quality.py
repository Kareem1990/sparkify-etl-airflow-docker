from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    Operator to run data quality checks on Redshift tables.
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        self.log.info(f"🚀 Starting data quality checks on tables: {self.tables}")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for table in self.tables:
            self.log.info(f"🔍 Checking table: {table}")
            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1 or records[0][0] < 1:
                raise ValueError(f"❌ Data quality check failed for table '{table}': No records found.")
            self.log.info(f"✅ Data quality check passed for table '{table}' with {records[0][0]} records.")
