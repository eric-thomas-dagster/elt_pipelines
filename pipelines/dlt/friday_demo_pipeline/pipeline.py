"""dlt pipeline: friday_demo_pipeline

Load github data to duckdb
"""

import dlt
from dlt.sources.github import github_reactions

def run(partition_key: str = None):
    """Run the GitHub pipeline."""

    # Configure the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="friday_demo_pipeline",
        destination="duckdb",
        dataset_name="github_REPO_OWNER_REPO_NAME",
    )

    # Load GitHub data
    # Access token will be read from GITHUB_TOKEN environment variable
    source = github_reactions(
        owner="REPO_OWNER",
        name="REPO_NAME",
        items_per_page=100,
        max_items=None,  # Load all data
    )

    # Select which resources to load
    resources_to_load = ["issues", "pull_requests"]
    source = source.with_resources(*resources_to_load)

    # Run the pipeline with write disposition
    info = pipeline.run(
        source,
        write_disposition="append",
        loader_file_format="parquet"  # File format for file-based destinations
    )

    print(f"Pipeline completed: {info}")
    return info

if __name__ == "__main__":
    import sys
    partition = sys.argv[1] if len(sys.argv) > 1 else None
    run(partition_key=partition)
