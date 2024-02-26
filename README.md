
# Aircraft Emissions

**Library version:** `0.1.0`

**Standards:** `CAEP/12` - `01 January 2023`

**ICAO Databank:** `v29B` - `20 June 2023`

---


The `aircraft_emissions` library gives access to ICAO's emission certification standards[^1][^2] and the  emissions databank of certified aircraft engines[^3]. Designed to support environmental compliance and analysis, this library facilitates:

- :triangular_flag_on_post: **Emission Certification:** Assists in ensuring compliance with international standards.
- :airplane: **Market Analysis:** Facilitates comparison of various aircraft engines.
- :art: **Data Visualization:** Offers tools for illustrating emissions and understanding trade-offs.

The library covers:
- Turbojet and turbofan engines with thrust greater than 26.7kN.
- Standards up to and including CAEP/12, applicable to both existing and newly introduced engine types from 1 January 2023.
- Pollutant emissions from engine exhaust, including gaseous pollutants (NOx, CO, HC, Smoke-Number) and non-volatile particulate matter (mass, number, and concentration).
- Subsonic and supersonic cycles.

<blockquote style="background-color: #ffffff; color: #333; border-left: 4px solid #ffa500; padding: 0.5em 10px; margin: 1em 0; box-shadow: 0 2px 15px rgba(0,0,0,0.1);">
  <strong>⚠️ Disclaimer</strong><br>
  This library is independent and not affiliated with any certifying organizations or manufacturers. Data is based on publicly available sources.
</blockquote>


# Installation
Please be aware that this repository does not host the complete source code of the library. Instead, detailed information about the use cases it covers and the functionalities it provides can be found within the documentation. 

For access to the full library, including the source code, please contact the author directly.

# Certification

The example provided below illustrates the certification of `NOx` emissions for the `PW1133G Block-D` engine, in accordance with the `CAEP/8` standard. It utilizes a specific `standard` along with a `Dataset` that includes pertinent data about the engine and the emissions recorded at the engine's exhaust.

For guidance on certifying both `gaseous` and `nvPM` emissions for engines under the `CAEP/12` standard, please consult the documentation for comprehensive details.

```python
from aircraft_emissions import certificate
from aircraft_emissions.datasets import Dataset, SubsonicPoints
from aircraft_emissions.standards.subsonic import StandardNoxCaep8

# PW1122G Block-D - UID:01P22PW158
dataset = Dataset(
    rated_thrust=107.82,
    opr=28.78,
    number_engines_tested=1,
    fuel_massflow=SubsonicPoints(0.710, 0.600, 0.210, 0.080),
    emissions=SubsonicPoints(18.206, 15.392, 10.422, 5.008),
)

# Certificate
certificate.emissions(dataset, StandardNoxCaep8)
```

Which gives the following result:
``` python
{
  'is_certified': True,
  'percent_of_limit': 64.7,
  'number_engines_tested': 1,
  'characteristic': 31.3
  'limit': 48.4,
}
```

# Market Data Analysis
Comparing multiple engines in terms of their environmental impact on air quality can be easily assessed. The following example compares the engines of the `Airbus A320 NEO` regarding `NOx` certification, illustrating their relative positioning to each other and their compliance with current standards.

This analysis can be extended to other engines, other pollutants, and different graphical representations. For more details, please refer to the documentation.

```python
from aircraft_emissions import plot

# Select engines available on the Airbus A320
engines = ['LEAP-1A 2019', "PW1100G Block-D"]

# Plot NOx certification values against standard limits
plot.characteristic.nox(engines)

# Plot nvPM Mass certification values against standard limits
plot.characteristic.nvpm_mass(engines)
```

![Plot NOx Characteristic](assets/plot_nox_characteristic.png)

# Visualizing emission trade-offs
Understanding the impact of technological choices on pollutant emissions is crucial. By visualizing the evolution of trade-offs for engines with new combustion chamber definitions, one can gain insights into the environmental implications of these technologies. 

The following example demonstrates the trade-off between `EINOx` and `EICO` for the `CFM56-7B` engine, comparing its performance at entry into service named `SAC` and after the emission certification update with the introduction of the `Tech Insertion` definition.

It can be observed that while the `Tech Insertion` definition has led to a reduction in `EINOx` emissions, this has been at the expense of `EICO`.

```python
from aircraft_emissions import plot

# Select CFM56-7B engines: entry into service (SAC) vs Tech Insertion update
engines = ["CFM56-7B SAC", "CFM56-7B Tech Insertion"]

# Visualize the NOx - CO trade-off
plot.gaseous_measures(x="thrust", y=['einox', 'eico'], engines)
```

![Plot trade-offs](assets/trade_offs_cfm56_7b.PNG)


[^1]: https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank

[^2]: https://ffac.ch/wp-content/uploads/2020/10/ICAO-Annex-16-Environmental-protection-Vol-II-Aircraft-Engine-Emissions.pdf

[^3]: https://www.easa.europa.eu/en/domains/environment/icao-aircraft-engine-emissions-databank