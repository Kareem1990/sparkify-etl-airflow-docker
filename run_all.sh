#!/bin/bash
set -e

echo "🔄 Loading environment variables from .env"
set -a
source .env
set +a

echo "🐍 Installing Python dependencies..."
pip install --quiet -r requirements.txt

echo "🚀 Running Terraform (init + apply)..."
terraform init
terraform apply -auto-approve

echo "✅ Terraform completed."

echo "🎯 Triggering Airflow DAG manually..."
docker exec -it sparkify-etl-airflow-docker-webserver-1 \
  airflow dags trigger sparkify_etl_dag

echo "🎉 All done. You're ready for the demo!"


# run_all.sh
#
# This script automates the full setup and execution of the Sparkify ETL project.
# It performs the following steps:
#   1. Loads environment variables from the .env file
#   2. Installs Python dependencies
#   3. Initializes and applies Terraform to provision AWS resources (Redshift, IAM, etc.)
#   4. Triggers the Airflow DAG inside the Docker container to start the ETL workflow
#
# Use this script to quickly bootstrap and test the entire pipeline end-to-end.