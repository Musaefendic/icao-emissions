## Disclaimer
- This package is not affiliated with the ICAO
- Not functional, work in progress

## Purpose 
- Give access to a **cleaned** version of the emission databank, in the form of a DataFrame. 
- Provide plotting presets for each engine model to help produce consistent figures.
- Provides a module to calculate the margins of gaseous and nvPM pollutant emissions, as defined by ICAO, in Annex 16, Volume II. 

## Load dataframes
- :white_check_mark: Gaseous Emissions `icao_emissions.databanks.load_gaseous_emissions()`
- :white_check_mark: Gaseous Certification `icao_emissions.databanks.load_gaseous_certification()`
- :x: nvPM  Emissions `icao_emissions.databanks.load_nvpm_emissions()`
- :x: nvPM Certification `icao_emissions.databanks.load_nvpm_certification()`

```python
import icao_emissions as icao

# Load the gaseous certification databank
df = icao.databanks.load_gaseous_certification()

# Select a reduced number of columns
df = df[['manufacturer', 'engine', 'bpr', 'opr', 'rated_thrust', 'hc_margin', 'co_margin', 'nox_caep8_margin']] 

# Select some engines
df[df['engine'].str.contains('|'.join(['LEAP-1A', 'PW1100G Block-D']), na=False)]
```

Output
|      | manufacturer    | engine          | bpr  | opr  | rated_thrust  | hc_margin  | co_margin  | nox_caep8_margin |
|------|-----------------|-----------------|------|------|---------------|------------|------------|------------------|
| 121  | CFM             | LEAP-1A 2017    | 11.1 | 33.4 | 120.6         | 2.4        | 25.1       | 45.7             |
| 122  | CFM             | LEAP-1A 2017    | 10.5 | 38.6 | 143.1         | 1.8        | 20.0       | 68.8             |
| 123  | CFM             | LEAP-1A 2019    | 11.3 | 30   | 106.8         | 3          | 31.0       | 48               |
| 124  | CFM             | LEAP-1A 2019    | 11.1 | 33.3 | 120.6         | 2.5        | 26.1       | 56.9             |
| 125  | CFM             | LEAP-1A 2019    | 10.7 | 35.5 | 130.3         | 2.2        | 23.4       | 74.5             |
| 126  | CFM             | LEAP-1A 2019    | 10.5 | 38.5 | 143.1         | 1.9        | 20.4       | 89.3             |
| 388  | Pratt & Whitney | PW1100G Block-D | 12.7 | 28.8 | 107.8         | 5.4        | 34.5       | 64.7             |
| 389  | Pratt & Whitney | PW1100G Block-D | 12.7 | 28.8 | 107.8         | 5.4        | 34.5       | 64.7             |
| 390  | Pratt & Whitney | PW1100G Block-D | 12.7 | 28.8 | 107.8         | 5.4        | 34.5       | 64.7             |
| 391  | Pratt & Whitney | PW1100G Block-D | 12.3 | 31.7 | 120.4         | 4.5        | 29.1       | 61.9             |
| 392  | Pratt & Whitney | PW1100G Block-D | 12.3 | 31.7 | 120.4         | 4.5        | 29.1       | 61.9             |
| 393  | Pratt & Whitney | PW1100G Block-D | 12.3 | 31.7 | 120.4         | 4.5        | 29.1       | 61.9             |
| 394  | Pratt & Whitney | PW1100G Block-D | 12   | 34   | 130.1         | 3.9        | 25.6       | 60.9             |
| 395  | Pratt & Whitney | PW1100G Block-D | 11.6 | 38.1 | 147.3         | 3.7        | 25.1       | 62.8             |
| 396  | Pratt & Whitney | PW1100G Block-D | 11.6 | 38.1 | 147.3         | 3.7        | 25.1       | 62.8             |
| 397  | Pratt & Whitney | PW1100G Block-D | 11.6 | 38.1 | 147.3         | 3.7        | 25.1       | 62.8             |


## Plot NOx Characteristic
```python
import icao_emissions as icao
from icao_emissions.plot import Figure, PlotNoxCharacteristic


# Load the gaseous certification databank
df = icao.databanks.load_gaseous_certification()

# Select some engines
df = df[df['engine'].str.contains('|'.join(['LEAP-1A', 'PW1100G Block-D']), na=False)]

# Plot
plot = PlotNoxCharacteristic(df)

figure = Figure()
figure.add(plot)
```

![Plot NOx Characteristic](assets/plot_nox_characteristic.png)

## Source
- https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank
- https://ffac.ch/wp-content/uploads/2020/10/ICAO-Annex-16-Environmental-protection-Vol-II-Aircraft-Engine-Emissions.pdf

