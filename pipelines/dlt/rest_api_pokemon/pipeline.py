"""Pokemon REST API to DuckDB Pipeline.

This pipeline extracts Pokemon data from the public PokeAPI and loads it into DuckDB.
Great for demos and testing - no authentication required!
"""

import dlt
from dlt.sources.helpers import requests


@dlt.source
def pokemon_source():
    """Load Pokemon data from the public PokeAPI."""

    @dlt.resource(write_disposition="replace", primary_key="id")
    def pokemon():
        """Extract Pokemon data."""
        base_url = "https://pokeapi.co/api/v2/pokemon"

        # Get first 151 Pokemon (original generation)
        for pokemon_id in range(1, 152):
            url = f"{base_url}/{pokemon_id}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            # Flatten the data for easier analysis
            pokemon_data = {
                "id": data["id"],
                "name": data["name"],
                "height": data["height"],
                "weight": data["weight"],
                "base_experience": data["base_experience"],
                "types": [t["type"]["name"] for t in data["types"]],
                "abilities": [a["ability"]["name"] for a in data["abilities"]],
                "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
            }

            yield pokemon_data

    @dlt.resource(write_disposition="replace", primary_key="id")
    def pokemon_types():
        """Extract Pokemon type information."""
        url = "https://pokeapi.co/api/v2/type"
        response = requests.get(url)
        response.raise_for_status()

        types_list = response.json()["results"]

        for type_info in types_list:
            type_response = requests.get(type_info["url"])
            type_response.raise_for_status()

            type_data = type_response.json()

            yield {
                "id": type_data["id"],
                "name": type_data["name"],
                "pokemon_count": len(type_data["pokemon"]),
            }

    return pokemon, pokemon_types


def run():
    """Execute the Pokemon API pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="pokemon_api",
        destination="duckdb",
        dataset_name="pokemon_data",
    )

    # Run the pipeline
    load_info = pipeline.run(pokemon_source())

    print(f"Pipeline completed: {load_info}")
    return load_info


if __name__ == "__main__":
    run()
