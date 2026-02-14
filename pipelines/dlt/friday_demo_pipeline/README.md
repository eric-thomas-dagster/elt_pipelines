# friday_demo_pipeline

Load github data to duckdb

## Source
- **Type**: github

### Configuration
- **repos**: dagster-io/dagster
- **resources**: ['issues', 'pull_requests']

## Destination
- **Type**: duckdb

## Run Locally

```bash
python -m pipelines.dlt.friday_demo_pipeline.pipeline
```

## Environment Variables

See your .env file for required credentials.
