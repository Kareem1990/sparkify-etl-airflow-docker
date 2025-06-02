#!/bin/bash
set -e  # Exit the script immediately if any command fails

echo "🔄 Loading environment variables from .env"
set -a                  # Export all variables defined from now on as environment variables
source .env             # Load environment variables from the .env file
set +a                  # Stop automatically exporting variables

echo "🐍 Installing Python dependencies..."
pip install --quiet -r requirements.txt  # Install Python packages listed in requirements.txt

echo "🚀 Running Terraform (init + apply)..."
terraform init                           # Initialize Terraform (downloads providers, sets up state)
terraform apply -auto-approve            # Apply Terraform plan to create AWS resources without prompting
echo "✅ Terraform completed."

echo "🐳 Starting Docker containers..."
docker-compose up -d --build             # Build and run Docker containers in detached mode

echo "⏳ Waiting for Airflow Webserver to be ready..."
sleep 15                                 # Wait a few seconds to let Airflow initialize

echo "🎯 Triggering Airflow DAG manually..."
docker exec -it sparkify-etl-airflow-docker-webserver-1 airflow dags trigger sparkify_etl_dag  # Trigger the ETL DAG manually from within the webserver container

echo "🎉 All done. You're ready for the demo!"  # Final success message


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
