from datetime import datetime, timedelta  # Used for scheduling and retry delays
from airflow import DAG  # Import DAG class to define workflows
from airflow.operators.dummy_operator import DummyOperator  # Dummy operator to mark start/end points
from airflow.providers.postgres.operators.postgres import PostgresOperator  # To run SQL on Redshift

from operators.stage_redshift import StageToRedshiftOperator  # Custom operator to copy data from S3 to Redshift
from operators.load_fact import LoadFactOperator  # Custom operator to load data into a fact table
from operators.load_dimension import LoadDimensionOperator  # Custom operator to load data into dimension tables
from operators.data_quality import DataQualityOperator  # Custom operator to run data quality checks
from helpers.sql_queries import SqlQueries  # Contains predefined SQL queries

# Default configuration for DAG tasks
default_args = {
    'owner': 'kareem',
    'start_date': datetime(2025, 1, 1),  # Start date of the DAG
    'depends_on_past': False,  # Tasks do not depend on previous runs
    'retries': 3,  # Number of retries on failure
    'retry_delay': timedelta(minutes=5),  # Delay between retries
    'catchup': False  # Do not backfill missed runs
}

# DAG definition block
with DAG('sparkify_etl_dag',
         default_args=default_args,
         description='Load and transform data in Redshift with Airflow',
         schedule_interval='@once',  # Run only once
         catchup=False,
         is_paused_upon_creation=False,
         max_active_runs=1,
         template_searchpath=['/opt/airflow/sql']  # Path for SQL files
         ) as dag:

    # Task: Run SQL script to create necessary tables
    create_tables = PostgresOperator(
        task_id='Create_tables',
        postgres_conn_id='redshift',
        sql='create_tables.sql'
    )

    # Task: Dummy operator to mark the beginning
    start_operator = DummyOperator(task_id='Begin_execution')

    # Task: Stage log data from Udacity's S3 bucket to Redshift
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_events',
        s3_bucket='udacity-dend',
        s3_key='log_data',
        copy_json_option='s3://udacity-dend/log_json_path.json',
        region='us-west-2'
    )

    # Task: Stage song data from Udacity's S3 bucket to Redshift
    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_songs',
        s3_bucket='udacity-dend',
        s3_key='song_data',
        copy_json_option='auto',
        region='us-west-2'
    )

    # Task: Load data into the songplays fact table
    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        table='songplays',
        sql_query=SqlQueries.songplay_table_insert,
        append_data=False  # Overwrite existing data
    )

    # Task: Load user dimension table
    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='users',
        sql_query=SqlQueries.user_table_insert,
        append_data=False
    )

    # Task: Load song dimension table
    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='songs',
        sql_query=SqlQueries.song_table_insert,
        append_data=False
    )

    # Task: Load artist dimension table
    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='artists',
        sql_query=SqlQueries.artist_table_insert,
        append_data=False
    )

    # Task: Load time dimension table
    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='time',
        sql_query=SqlQueries.time_table_insert,
        append_data=False
    )

    # Task: Run data quality checks on all target tables
    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id='redshift',
        tables=['songplays', 'users', 'songs', 'artists', 'time']
    )

    # Task: Dummy operator to mark the end
    end_operator = DummyOperator(task_id='Stop_execution')

    # Task dependencies definition
    create_tables >> start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table

    load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table
    ] >> run_quality_checks >> end_operator

# Optional documentation string
dag.doc_md = __doc__
