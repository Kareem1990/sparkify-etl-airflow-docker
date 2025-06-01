#!/bin/bash
set -e

echo "🔄 Loading environment variables from .env"
set -a
source .env
set +a

echo "🚀 Running Terraform (init + apply)..."
terraform init
terraform apply -auto-approve

echo "✅ Terraform completed."

echo "🎯 Triggering Airflow DAG manually..."
docker exec -it sparkify-etl-airflow-docker-webserver-1 \
  airflow dags trigger sparkify_etl_dag

echo "🎉 All done. You're ready for the demo!"
