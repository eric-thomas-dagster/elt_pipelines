# demo_pipeline_friday

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
python -m pipelines.dlt.demo_pipeline_friday.pipeline
```

## Environment Variables

See your .env file for required credentials.
