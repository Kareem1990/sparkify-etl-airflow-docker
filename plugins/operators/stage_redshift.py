from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    # Enables templating for dynamic s3_key values using context (e.g., {{ ds }})
    template_fields = ("s3_key",)

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 copy_json_option="auto",
                 region="us-west-2",  # Region of Udacity S3 bucket
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket  # Fixed bucket name for Udacity data
        self.s3_key = s3_key
        self.copy_json_option = copy_json_option
        self.region = region

    def execute(self, context):
        # Fetch AWS credentials from Airflow connection
        s3_hook = S3Hook(self.aws_credentials_id)
        credentials = s3_hook.get_credentials()

        # Connect to Redshift
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Clear existing data in the target table
        self.log.info(f"Clearing data from Redshift table {self.table}")
        redshift.run(f"DELETE FROM {self.table}")

        # Format S3 path using runtime context
        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        # Execute COPY command to load data
        copy_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{credentials.access_key}'
            SECRET_ACCESS_KEY '{credentials.secret_key}'
            REGION '{self.region}'
            FORMAT AS JSON '{self.copy_json_option}';
        """

        self.log.info(f"Copying data from {s3_path} to Redshift table {self.table}")
        redshift.run(copy_sql)
