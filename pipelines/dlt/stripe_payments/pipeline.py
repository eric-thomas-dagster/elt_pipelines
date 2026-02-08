"""Stripe Payments to DuckDB Pipeline.

This pipeline extracts payment and customer data from Stripe and loads it into DuckDB.
"""

import dlt
from dlt.sources.helpers import requests


@dlt.source
def stripe_source(api_key: str = dlt.secrets.value):
    """Load payments, customers, and charges from Stripe API."""

    @dlt.resource(write_disposition="merge", primary_key="id")
    def payments():
        """Extract payment intents from Stripe."""
        url = "https://api.stripe.com/v1/payment_intents"
        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        yield data.get("data", [])

    @dlt.resource(write_disposition="merge", primary_key="id")
    def customers():
        """Extract customers from Stripe."""
        url = "https://api.stripe.com/v1/customers"
        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        yield data.get("data", [])

    return payments, customers


def run():
    """Execute the Stripe pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="stripe_payments",
        destination="duckdb",
        dataset_name="stripe_data",
    )

    # Run the pipeline
    load_info = pipeline.run(stripe_source())

    print(f"Pipeline completed: {load_info}")
    return load_info


if __name__ == "__main__":
    run()
