"""Hacker News pipeline using DLT REST API source.

This pipeline demonstrates using the generic REST API source instead of custom Python code.
Uses the Algolia-powered HackerNews Search API for simpler configuration.
"""

import dlt
from dlt.sources.rest_api import rest_api_source

def run(partition_key: str = None):
    """Run the HackerNews REST API pipeline.

    Args:
        partition_key: Partition key for partitioned assets (e.g., "2024-01-01")
    """

    # Configure the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="hackernews_rest",
        destination="duckdb",
        dataset_name="hackernews_data",
    )

    # Configure REST API source using Algolia HackerNews API
    # This is simpler than the Firebase API as it returns full story data in one request
    source = rest_api_source({
        "client": {
            "base_url": "https://hn.algolia.com/api/v1",
        },
        "resources": [
            {
                "name": "top_stories",
                "endpoint": {
                    "path": "search",
                    "params": {
                        "tags": "front_page",
                        "hitsPerPage": 50,
                    },
                },
                "data_selector": "hits",
            },
            {
                "name": "best_stories",
                "endpoint": {
                    "path": "search",
                    "params": {
                        "tags": "story",
                        "numericFilters": "points>100",
                        "hitsPerPage": 30,
                    },
                },
                "data_selector": "hits",
            }
        ]
    })

    # Run the pipeline with replace disposition (full refresh)
    info = pipeline.run(
        source,
        write_disposition="replace"
    )

    print(f"Pipeline completed: {info}")
    return info

if __name__ == "__main__":
    import sys
    partition = sys.argv[1] if len(sys.argv) > 1 else None
    run(partition_key=partition)
