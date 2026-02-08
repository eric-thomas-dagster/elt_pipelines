#!/bin/bash
# Quick script to run pipelines

set -e

echo ""
echo "========================================"
echo "  ELT Pipeline Runner"
echo "========================================"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo ""
    echo "Please create a .env file from .env.example:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env with your credentials"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Menu
echo "Select a pipeline to run:"
echo ""
echo "  1) GitHub Issues (dlt)"
echo "  2) Postgres to DuckDB (Sling)"
echo "  3) Run all pipelines"
echo "  4) Launch Dagster UI"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Running GitHub Issues pipeline..."
        echo ""
        cd pipelines/dlt/github_issues
        python pipeline.py
        ;;
    2)
        echo ""
        echo "Running Postgres to DuckDB replication..."
        echo ""
        cd pipelines/sling/postgres_to_duckdb
        sling run -r replication.yaml
        ;;
    3)
        echo ""
        echo "Running all pipelines..."
        echo ""

        echo "→ GitHub Issues..."
        cd pipelines/dlt/github_issues
        python pipeline.py
        cd ../../..

        echo ""
        echo "→ Postgres to DuckDB..."
        cd pipelines/sling/postgres_to_duckdb
        sling run -r replication.yaml
        cd ../../..

        echo ""
        echo "✅ All pipelines completed!"
        ;;
    4)
        echo ""
        echo "Launching Dagster UI..."
        echo ""
        echo "Make sure you have installed dagster_elt_project:"
        echo "  cd ../dagster_elt_project && pip install -e ."
        echo ""
        read -p "Press Enter to continue or Ctrl+C to cancel..."

        cd ../dagster_elt_project
        dagster dev
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "  Done!"
echo "========================================"
echo ""
