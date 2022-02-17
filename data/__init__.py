"""This module contains all data ressources, which are not code files.

The resources are organised in two sub-folders.
    └── data/
        ├── icao_databank/
        └── themes/

The 'icao_databank' repository contains:
    - The *raw* emissions databank.
    - The *cleaned* emissions databank.
    - All scripts needed to get the cleaned file from the raw file.

The 'themes' repository contains:
    - Graphic themes used to generate plots.
    - Each engine is caracterised by a plotting style (symbol, color, ...).


For developer's use:
    - The data resources could be retrieved from the source code.
    - The pkg_resources library should be used. An example is given below.

    import pkg_resources
    data = pkg_resources.resource_string('data', 'icao_databank/edb.csv')
"""
