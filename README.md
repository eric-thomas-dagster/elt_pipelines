# ELT Pipelines Example Project

A standalone Python project demonstrating ELT pipelines using **dlt** and **Sling**. These pipelines work independently but are **even better with Dagster** for orchestration, scheduling, and monitoring.

## 📋 What's Inside

This project contains two example pipelines:

### 1. **GitHub Issues** (dlt)
- **Source**: GitHub API
- **Destination**: DuckDB (configurable)
- **Data**: Issues, Pull Requests, Commits
- **Location**: `pipelines/dlt/github_issues/`

### 2. **Postgres to DuckDB** (Sling)
- **Source**: PostgreSQL database
- **Destination**: DuckDB
- **Data**: Users, Orders, Products tables
- **Location**: `pipelines/sling/postgres_to_duckdb/`

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install dlt with DuckDB support
pip install "dlt[duckdb]"

# Install Sling
pip install sling

# Optional: Install Dagster for orchestration
pip install dagster dagster-webserver
```

### 2. Set Up Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env
```

At minimum, you need:
- `GITHUB_TOKEN` - For the GitHub pipeline
- `POSTGRES_*` credentials - For the Sling replication

### 3. Run Pipelines Standalone

**Run the dlt pipeline:**
```bash
cd pipelines/dlt/github_issues
python pipeline.py
```

**Run the Sling replication:**
```bash
cd pipelines/sling/postgres_to_duckdb
sling run -r replication.yaml
```

---

## 🎯 Using with Dagster (Recommended!)

While these pipelines work standalone, **Dagster makes them better** by providing:
- ✅ **Scheduling** - Run pipelines on a schedule
- ✅ **Monitoring** - Track pipeline runs and failures
- ✅ **Orchestration** - Manage dependencies between pipelines
- ✅ **Observability** - View logs, metrics, and data lineage
- ✅ **Testing** - Test pipelines before production

### Install Dagster Integration

```bash
# Install the dagster_elt_project package
cd ../dagster_elt_project
pip install -e .
```

### Run with Dagster

```bash
# Start Dagster UI
dagster dev

# Open http://localhost:3000
# Your pipelines will appear as assets!
```

### What You Get in Dagster

1. **Asset View** - See all your pipelines as assets
2. **Lineage Graph** - Understand data flow
3. **Schedules** - Pipelines run automatically based on `dagster.yaml`
4. **Run History** - Track every pipeline execution
5. **Logs** - Full observability into what happened
6. **Materialize** - Run pipelines on-demand from the UI

---

## 📁 Project Structure

```
elt_pipelines_example/
├── pipelines/
│   ├── dlt/
│   │   └── github_issues/
│   │       ├── pipeline.py       # Python code for dlt
│   │       ├── dagster.yaml      # Dagster configuration
│   │       └── config.yaml       # Pipeline metadata
│   └── sling/
│       └── postgres_to_duckdb/
│           ├── replication.yaml  # Sling configuration
│           ├── dagster.yaml      # Dagster configuration
│           └── config.yaml       # Pipeline metadata
├── .env.example                  # Environment variables template
├── .env                          # Your credentials (git-ignored)
├── README.md                     # This file
└── pyproject.toml               # Python package config
```

---

## 🔧 Configuration Files

Each pipeline has three configuration files:

### 1. **pipeline.py** or **replication.yaml**
The actual pipeline code/configuration that runs the ETL.

### 2. **dagster.yaml** (Dagster Configuration)
```yaml
enabled: true
description: "Pipeline description"
group: "asset_group"
schedule:
  enabled: true
  cron: "0 2 * * *"  # Daily at 2 AM
  timezone: "UTC"
```

### 3. **config.yaml** (Pipeline Metadata)
```yaml
source_type: "github"
destination_type: "duckdb"
source_configuration:
  repos: "dlt-hub/dlt"
  resources: ["issues", "pull_requests"]
tool: "dlt"
```

---

## 📝 Customizing Pipelines

### Modify GitHub Pipeline

Edit `pipelines/dlt/github_issues/pipeline.py`:

```python
# Change repositories
repos = ["your-org/your-repo", "another-org/another-repo"]

# Change resources to load
resources = ["issues", "pull_requests", "commits", "stargazers"]

# Change destination
pipeline = dlt.pipeline(
    pipeline_name="github_issues",
    destination="snowflake",  # or "bigquery", "redshift", etc.
    dataset_name="github_data"
)
```

### Modify Sling Replication

Edit `pipelines/sling/postgres_to_duckdb/replication.yaml`:

```yaml
streams:
  # Add more tables
  public.customers:
    mode: incremental
    primary_key: id
    update_key: updated_at

  # Sync entire schema
  public.*:
    mode: full-refresh
    object: "{stream_table}"
```

---

## 🎨 Creating New Pipelines

You can create new pipelines using the `elt` CLI tool:

```bash
# Install the ELT Builder
pip install -e ../embedded_elt_builder

# Create a new pipeline interactively
elt scaffold create stripe_to_snowflake \
  --source stripe \
  --destination snowflake

# Or use the Web UI
elt ui
```

The new pipeline will be automatically discovered by Dagster!

---

## 🧪 Testing

### Test dlt Pipeline

```bash
cd pipelines/dlt/github_issues

# Run with test data
GITHUB_REPOS="dlt-hub/dlt" python pipeline.py

# Check the output
duckdb data.duckdb "SELECT COUNT(*) FROM github_data.dlt_issues"
```

### Test Sling Replication

```bash
cd pipelines/sling/postgres_to_duckdb

# Dry run (shows what would be synced)
sling run -r replication.yaml --dry-run

# Run actual replication
sling run -r replication.yaml
```

---

## 🚨 Troubleshooting

### Pipeline Not Running?

1. **Check credentials** - Verify `.env` file has correct values
2. **Check enabled status** - Ensure `enabled: true` in `dagster.yaml`
3. **Check logs** - Look for error messages in terminal or Dagster UI
4. **Check dependencies** - Ensure dlt/sling are installed

### Dagster Not Discovering Pipelines?

1. **Check file structure** - Ensure all required files exist
2. **Check enabled status** - Must be `enabled: true`
3. **Refresh Dagster** - Reload definitions in Dagster UI
4. **Check paths** - Ensure Dagster can find the pipelines directory

### GitHub Rate Limiting?

- Add `GITHUB_TOKEN` to `.env`
- GitHub allows 5,000 requests/hour with a token vs 60/hour without

### Postgres Connection Failed?

- Verify `POSTGRES_*` credentials in `.env`
- Check that Postgres is running and accessible
- Test connection: `psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE`

---

## 📚 Learn More

### dlt Documentation
- [dlt Docs](https://dlthub.com/docs)
- [dlt Sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources)
- [dlt Destinations](https://dlthub.com/docs/dlt-ecosystem/destinations)

### Sling Documentation
- [Sling Docs](https://docs.slingdata.io)
- [Sling Connectors](https://docs.slingdata.io/connections)
- [Sling Replication](https://docs.slingdata.io/sling-cli/run)

### Dagster Documentation
- [Dagster Docs](https://docs.dagster.io)
- [Asset Definitions](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [Scheduling](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules)

---

## 💡 Next Steps

1. **Customize the examples** - Modify pipelines for your data sources
2. **Add more pipelines** - Create pipelines for other sources
3. **Set up Dagster** - Get full orchestration and monitoring
4. **Deploy to production** - Use Dagster Cloud or self-hosted Dagster
5. **Add tests** - Write tests for your pipeline logic
6. **Monitor data quality** - Add data quality checks

---

## 🤝 Contributing

Have improvements or new pipeline examples? Feel free to add them!

Common patterns to add:
- API sources (Stripe, Salesforce, HubSpot)
- Database replications (MySQL, MongoDB)
- Cloud storage (S3, GCS, Azure Blob)
- Analytics platforms (Google Analytics, Mixpanel)

---

## 📄 License

This example project is provided as-is for learning and demonstration purposes.

---

## 🎉 Summary

This project shows you how to:
- ✅ Write ELT pipelines with **dlt** (Python) and **Sling** (YAML)
- ✅ Run pipelines **standalone** without orchestration
- ✅ Make them **better with Dagster** for scheduling and monitoring
- ✅ Configure pipelines with YAML files
- ✅ Handle credentials securely with `.env` files

**Standalone is good. With Dagster is great!** 🚀
