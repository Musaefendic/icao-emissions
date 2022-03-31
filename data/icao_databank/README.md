Provide the ***raw*** emission databank, as downloaded from the ICAO website:
- source: https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank

Although the data contained within the emission databank is structured and cleaned, some operations are made to facilitate its use, such as:
- Remove duplicate rows
- Update model names to correctly reflect the evolution of engine definitions. Example: TRENT1000 Pack-B1, TRENT1000 Pack-C1, TRENT1000 TEN. 

For more details, see cleaning scripts available in the repository: 
- data/icao_edb/scripts