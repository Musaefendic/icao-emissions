"""Helper function to compute hash key."""

import hashlib
import os
from typing import AnyStr, Union


def compute_key(filename: Union[str, bytes, os.PathLike[AnyStr]]) -> str:
    """Read file as stream and compute hash key, based on hashlib.sha256."""
    hasher = hashlib.sha256()

    with open(filename, "rb") as infile:
        while True:
            chunk = infile.read(hasher.block_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()
