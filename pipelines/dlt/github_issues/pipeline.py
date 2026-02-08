"""
GitHub Issues dlt Pipeline

This pipeline loads GitHub issues, pull requests, and commits from specified repositories.

Usage:
    python pipeline.py
"""

import os
import dlt
from dlt.sources.helpers import requests


@dlt.source
def github_source(repos: list[str], resources: list[str] = None):
    """
    Load data from GitHub repositories.

    Args:
        repos: List of repositories in format "owner/repo"
        resources: List of resources to load (issues, pull_requests, commits)
    """
    if resources is None:
        resources = ["issues", "pull_requests"]

    for repo in repos:
        owner, repo_name = repo.split("/")

        if "issues" in resources:
            yield dlt.resource(
                fetch_issues(owner, repo_name),
                name=f"{repo_name}_issues",
                write_disposition="merge",
                primary_key="id"
            )

        if "pull_requests" in resources:
            yield dlt.resource(
                fetch_pull_requests(owner, repo_name),
                name=f"{repo_name}_pull_requests",
                write_disposition="merge",
                primary_key="id"
            )

        if "commits" in resources:
            yield dlt.resource(
                fetch_commits(owner, repo_name),
                name=f"{repo_name}_commits",
                write_disposition="append",
                primary_key="sha"
            )


def fetch_issues(owner: str, repo: str):
    """Fetch issues from a GitHub repository."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"state": "all", "per_page": 100}

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        # Filter out pull requests (they appear in issues endpoint)
        issues = [item for item in data if "pull_request" not in item]

        yield issues

        # Pagination
        if "next" in response.links:
            url = response.links["next"]["url"]
            params = {}  # URL already includes params
        else:
            break


def fetch_pull_requests(owner: str, repo: str):
    """Fetch pull requests from a GitHub repository."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {"state": "all", "per_page": 100}

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        yield response.json()

        # Pagination
        if "next" in response.links:
            url = response.links["next"]["url"]
            params = {}
        else:
            break


def fetch_commits(owner: str, repo: str):
    """Fetch commits from a GitHub repository."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": 100}

    page_count = 0
    max_pages = 10  # Limit to avoid too much data

    while url and page_count < max_pages:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        yield response.json()

        page_count += 1

        # Pagination
        if "next" in response.links and page_count < max_pages:
            url = response.links["next"]["url"]
            params = {}
        else:
            break


def run():
    """Run the pipeline - entry point for Dagster."""
    # Configuration
    repos = os.getenv("GITHUB_REPOS", "dlt-hub/dlt").split(",")
    resources = os.getenv("GITHUB_RESOURCES", "issues,pull_requests").split(",")

    # Destination
    destination_type = os.getenv("DESTINATION_TYPE", "duckdb")

    print(f"\n{'='*60}")
    print(f"  GitHub Issues Pipeline")
    print(f"{'='*60}")
    print(f"\n  Repositories: {', '.join(repos)}")
    print(f"  Resources: {', '.join(resources)}")
    print(f"  Destination: {destination_type}")
    print(f"\n{'='*60}\n")

    # Create pipeline
    pipeline = dlt.pipeline(
        pipeline_name="github_issues",
        destination=destination_type,
        dataset_name="github_data",
    )

    # Run pipeline
    source = github_source(repos=repos, resources=resources)
    load_info = pipeline.run(source)

    print(f"\n✅ Pipeline completed successfully!")
    print(f"   Loaded packages: {len(load_info.loads_ids)}")
    print(f"   Dataset: {pipeline.dataset_name}")

    return load_info


def main():
    """Standalone entry point."""
    return run()


if __name__ == "__main__":
    main()
