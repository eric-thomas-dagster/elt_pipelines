"""Hacker News top stories pipeline using dlt."""

import dlt
import requests
from typing import Iterator, Dict, Any


@dlt.resource(name="top_stories", write_disposition="replace")
def get_top_stories(max_items: int = 50) -> Iterator[Dict[str, Any]]:
    """Fetch top stories from Hacker News API."""
    # Get top story IDs
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()[:max_items]

    # Fetch each story
    for story_id in story_ids:
        story_response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()

        if story:
            yield {
                "id": story.get("id"),
                "title": story.get("title"),
                "url": story.get("url"),
                "score": story.get("score"),
                "by": story.get("by"),
                "time": story.get("time"),
                "type": story.get("type"),
                "descendants": story.get("descendants", 0),
            }


@dlt.resource(name="best_stories", write_disposition="replace")
def get_best_stories(max_items: int = 30) -> Iterator[Dict[str, Any]]:
    """Fetch best stories from Hacker News API."""
    response = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json")
    story_ids = response.json()[:max_items]

    for story_id in story_ids:
        story_response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()

        if story:
            yield {
                "id": story.get("id"),
                "title": story.get("title"),
                "url": story.get("url"),
                "score": story.get("score"),
                "by": story.get("by"),
                "time": story.get("time"),
                "type": story.get("type"),
            }


def run(partition_key: str = None):
    """Execute the Hacker News pipeline.

    Args:
        partition_key: Partition key for partitioned assets (e.g., "2024-01-01")
    """
    # Configure the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="hackernews",
        destination="duckdb",
        dataset_name="hackernews_data",
    )

    # Run the pipeline
    load_info = pipeline.run([get_top_stories(), get_best_stories()])
    print(f"Pipeline completed: {load_info}")
    return load_info


if __name__ == "__main__":
    run()
