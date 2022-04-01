"""
Functions to help validate the classification of engines.

What this module DOES NOT DO:
- Automatic classification of data

What this module DO:
- Check from plots that the classification made seems coherent
- Example: no discontinuity in the evolution of the polluting emissions according to the thrust

It is obvious that plotting the thrust emissions does not make sense. 
NOx production is not directly correlated with thrust. 
It would be more relevant to correlate this evolution with a variable related to the combustion chamber, i.e. a residence time or a combustion temperature. 
As these data are not public, it is not possible to use these metrics to classify the data.


It is sometimes difficult to follow and identify the evolutions of an engine in the ICAO databank. 
To facilitate the analysis, the ICAO databank contained in this library adds a new column: model.

Let us take the example of the LEAP-1A26 engine, in the v28 version of the ICAO database, there are several references for this model, but not clearly defined
- uid: 17CM082
- uid: 20CM089

The databank contained in this library will do this following classification:
- LEAP-1A 2017
- LEAP-1A 2019
"""

import importlib.resources
from typing import List, NoReturn, Optional, Tuple, TypedDict

import numpy as np
import pandas as pd
import yaml
from icao_emissions.databank import readers
from matplotlib import pyplot as plt

PlotParameters = TypedDict(
    "PlotParameters",
    {
        "x_axis": str,
        "y_axis": str,
        "xlim": Optional[List[float]],
        "ylim": Optional[List[float]],
        "polynomial_order": Optional[int],
    },
)


def load_parameters(filename: str) -> dict:
    # Init
    repository = "data.icao_databank.configs.validate"

    # Import the file
    with importlib.resources.open_binary(repository, filename) as infile:
        plot_parameters = yaml.safe_load(infile)

    return plot_parameters


ENGINE_IDENTIFICATION = load_parameters("engine_identification.yaml")
PLOT_PARAMETERS = load_parameters("plot_parameters.yaml")


def get_databank_per_engine(
    databank: pd.DataFrame, engine_identification: str
) -> dict[pd.DataFrame]:
    # engines of interest
    engines_of_interest = databank[
        databank["engine"].str.contains(engine_identification, na=False)
    ]

    # get versions available for a particular engine
    engine_versions = engines_of_interest["engine"].unique()

    databank_per_engine_version = {}
    # split engines
    for version in engine_versions:
        # extract
        databank_extract = databank[databank["engine"] == version]
        # save
        databank_per_engine_version[version] = databank_extract

    return databank_per_engine_version


def create_figure() -> Tuple[plt.Figure, Tuple[plt.Axes]]:
    return plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10, 6),
    )


def set_figure_limits(
    axes: Tuple[plt.Axes],
    xlim: Optional[List[float]],
    ylim: Optional[List[float]],
) -> Tuple[plt.Axes]:
    if xlim:
        axes[0].set_xlim(xlim)
        axes[1].set_xlim(xlim)

    if ylim:
        axes[0].set_ylim(ylim)
        axes[1].set_ylim(ylim)

    return axes


def get_colormap() -> List[str]:
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    return prop_cycle.by_key()["color"]


def plot_icao_databank(
    axes: Tuple[plt.Axes],
    databank: pd.DataFrame,
    x_axis: str,
    y_axis: str,
) -> Tuple[plt.Axes]:
    axes[0].scatter(x=databank[x_axis], y=databank[y_axis], c="grey", s=3)
    axes[1].scatter(x=databank[x_axis], y=databank[y_axis], c="grey", s=3)
    return axes


def add_polynomial_regression(axe, x, y, polynomial_order, color):
    coefs = np.polyfit(x, y, polynomial_order)
    interpolator = np.poly1d(coefs)

    _min = x.min()
    _max = x.max()

    axis_interpolater = np.linspace(_min, _max)
    axe.plot(
        axis_interpolater,
        interpolator(axis_interpolater),
        c=color,
    )


def plot_figure(
    icao_databank: pd.DataFrame,
    engine_databank: pd.DataFrame,
    plot_params: PlotParameters,
):
    # extract plot parameters
    x_axis = plot_params["x_axis"]
    y_axis = plot_params["y_axis"]
    xlim = plot_params.get("xlim")
    ylim = plot_params.get("ylim")
    polynomial_order = plot_params.get("polynomial_order")

    # create the figure
    _, axes = create_figure()

    #
    axes = set_figure_limits(axes, xlim, ylim)

    # get list of default matplotlib colors
    colors = get_colormap()

    # populate with all engines contained in the ICAO emissions databank
    axes = plot_icao_databank(axes, icao_databank, x_axis, y_axis)

    for index, (model_name, data) in enumerate(engine_databank.items()):
        data = data.sort_values(by=[x_axis])

        # Left plot
        axes[0].scatter(x=data[x_axis], y=data[y_axis], c="r", s=5)

        # add labels
        axes[0].set_xlabel(x_axis)
        axes[0].set_ylabel(y_axis)

        if polynomial_order:
            add_polynomial_regression(
                axes[1],
                data[x_axis],
                data[y_axis],
                polynomial_order,
                colors[index],
            )
            marker = "o"
        else:
            marker = "-o"

        # Right side plot
        axes[1].plot(
            data[x_axis],
            data[y_axis],
            marker,
            c=colors[index],
            markersize=3,
            label=model_name,
        )

        axes[1].legend()

        # add labels
        axes[1].set_xlabel(x_axis)
        axes[1].set_ylabel(y_axis)


def main(
    engine_name: str, engine_identification: str, plot_parameters: dict
) -> NoReturn:
    # import certification databank
    databanks = {
        "certification": readers.get_certification_databank("gaseous"),
        "emissions": readers.get_emissions_databank("gaseous"),
    }

    for _, params in plot_parameters.items():
        # get the proper databank : certification or emissions
        databank = databanks[params["databank"]]

        # get
        dataframes_per_engine = get_databank_per_engine(
            databank, engine_identification
        )

        # plot
        plot_figure(
            databank,
            dataframes_per_engine,
            params,
        )

    # show plots
    plt.legend()
    plt.show()


if __name__ == "__main__":
    engine_name = "PW1200G"

    # get parameters associated of the engine of interest
    engine_identification = ENGINE_IDENTIFICATION[engine_name]
    plot_parameters = PLOT_PARAMETERS[engine_name]

    # evaluate classification based on plots
    main(engine_name, engine_identification, plot_parameters)
