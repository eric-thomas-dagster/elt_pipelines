"""Jokes pipeline using dlt - fetches programming jokes from JokeAPI."""

import dlt
import requests
from typing import Iterator, Dict, Any


@dlt.resource(name="programming_jokes", write_disposition="append")
def get_programming_jokes(count: int = 10) -> Iterator[Dict[str, Any]]:
    """Fetch programming jokes from JokeAPI."""
    for i in range(count):
        response = requests.get(
            "https://v2.jokeapi.dev/joke/Programming",
            params={"type": "single"}
        )
        joke_data = response.json()

        if not joke_data.get("error"):
            yield {
                "id": joke_data.get("id"),
                "joke": joke_data.get("joke"),
                "category": joke_data.get("category"),
                "language": joke_data.get("lang"),
                "safe": joke_data.get("safe"),
            }


def run(partition_key: str = None):
    """Execute the jokes pipeline.

    Args:
        partition_key: Partition key for partitioned assets (e.g., "2024-01-01")
    """
    # Configure the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="jokes",
        destination="duckdb",
        dataset_name="jokes_data",
    )

    # Run the pipeline
    load_info = pipeline.run(get_programming_jokes())
    print(f"Pipeline completed: {load_info}")
    return load_info


if __name__ == "__main__":
    run()
