## Disclaimer
- This package is not affiliated with the ICAO

## Purpose
This library is designed to facilitate interaction with the International Civil Aviation Organization (ICAO) emission databanks, which include noise and emissions data. This library provides users with the following features: 

🗂 Access to icao databanks: noise and emissions<br>
🎛 Calculate the certification data (characteristic value, margin, ...)<br>
📈 Visualization of databanks in relation to regulatory standards


This library is perfect for researchers, engineers, policy-makers, and enthusiasts looking to analyze and visualize aviation emission data.

## Emission Standards and certification

<details>  
  <summary> 💈 Here is the status of standards available within the library: </summary>
  
|  | subsonic | supersonic |
|---|:---:|:---:|
| NOx - CAEE | ❌ | ❌ |
| NOx - CAEP/2 | ✅ | ❌ |
| NOx - CAEP/4 | ❌ | ❌ |
| NOx - CAEP/6 | ❌ | ❌ |
| NOx - CAEP/8 | ✅ | ❌ |
| CO | ❌ | ❌ |
| UHC | ❌ | ❌ |
| nvPM - concentration | ❌ | ❌ |
| nvPM - mass | ❌ | ❌ |
| nvPM - number | ❌ | ❌ |

 </details>

```python
import pprint
from icao_emissions.certification import nox_caep8, EmissionData

nox_emissions = EmissionData(
    rated_thrust=147.28,
    opr=38.85,
    number_engines_tested=1,
    emissions=(25.23, 18.92, 9.14, 6.98),
    fuel_massflow=(1.0230, 0.8385, 0.2783, 0.0988),
)

nox_certification = nox_caep8.certificate(nox_emissions)

pprint.pprint(nox_certification)
```
```
CertificationData(rated_thrust=147.3,
                  opr=38.9,
                  number_engines_tested=1,
                  characteristic=38.3,
                  limit=67.8,
                  margin=-0.4,
                  is_certified=True,
                  total_emission_mass=4864.4,
                  total_fuel_mass=374.6)
```

## Plot NOx Characteristic
```python
from icao_emissions import databanks
from icao_emissions.plot import Figure, PlotNoxCharacteristic


# Load the gaseous certification databank
df = databanks.load_gaseous_certification()

# Select some engines
query = {'engine': ('LEAP-1A', 'PW1100G Block-D')}
df = databanks.filter(df, query)

# Plot
plot = PlotNoxCharacteristic(df)

figure = Figure()
figure.add(plot)
```

![Plot NOx Characteristic](assets/plot_nox_characteristic.png)

## Source
- https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank
- https://ffac.ch/wp-content/uploads/2020/10/ICAO-Annex-16-Environmental-protection-Vol-II-Aircraft-Engine-Emissions.pdf

