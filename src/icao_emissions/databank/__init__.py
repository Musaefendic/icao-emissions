"""Give access to ICAO emissions databank."""

from icao_emissions.databank import readers

edb_raw = readers.get_raw_icao_databank()
