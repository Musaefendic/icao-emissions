import os

import yaml
from icao_emissions.utils import hashing


def main() -> None:
    """Generate hash keys for tracked files."""
    # generate hash_keys
    hash_keys = hashing.generate_hash_keys()

    # get location of this python script
    filename = "hash_keys.yaml"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # write 'hash_keys.yaml'
    with open(filepath, "w") as outfile:
        yaml.safe_dump(hash_keys, outfile, default_flow_style=False)


if __name__ == "__main__":
    main()
