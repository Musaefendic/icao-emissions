# from typing import Tuple

# import matplotlib
# import numpy as np
# import pandas as pd
# from icao_emissions.databank import readers
# from matplotlib import pyplot as plt

# MODELS_IDENTIFICATION = {
#     "PW1100G": "PW11",
# }


def extract_emissions(databank: pd.DataFrame) -> pd.DataFrame:
    # init
    emissions = pd.DataFrame()

    # columns to extract
    emission_suffix = ["_take_off", "_climb", "_approach", "_idle"]
    emissions_columns = {"einox": {}, "eico": {}, "eihc": {}}

    #
    for emission_name in emissions_columns:
        emissions_columns[emission_name] = [
            emission_name + prefix for prefix in emission_suffix
        ]

    thrust_columns = [
        "thrust_take_off",
        "thrust_climb",
        "thrust_approach",
        "thrust_idle",
    ]

    for _, row in databank.iterrows():
        temporary_df = pd.DataFrame(
            {
                "thrust": row[thrust_columns].values,
                "ienox": row[emissions_columns["einox"]].values,
                "ieco": row[emissions_columns["eico"]].values,
                "iehc": row[emissions_columns["eihc"]].values,
            }
        )

        # stack
        emissions = pd.concat([emissions, temporary_df], ignore_index=True)

    return emissions


# def create_figure(nrows: int, ncols: int) -> Tuple[plt.Figure, Tuple[plt.Axes]]:
#     return plt.subplots(
#         nrows=nrows,
#         ncols=ncols,
#         figsize=(10, 6),
#     )


# def plot_figure(
#     databank: pd.DataFrame, engines: pd.DataFrame, plot_params: dict
# ):
#     # extract
#     x_axis = plot_params.get("x_axis")
#     y_axis = plot_params.get("y_axis")
#     xlim = plot_params.get("xlim")
#     ylim = plot_params.get("ylim")
#     polynomial_order = plot_params.get("polynomial_order")

#     number_rows = 1
#     number_columns = 2

#     # create subplots
#     fig, axes = create_figure(number_rows, number_columns)

#     # populate with all engines contained in the ICAO emissions databank
#     axes = plot_all_engines(axes, databank, x_axis, y_axis)

#     if xlim:
#         axes[0].set_xlim(xlim)
#         axes[1].set_xlim(xlim)

#     if ylim:
#         axes[0].set_ylim(ylim)
#         axes[1].set_ylim(ylim)

#     prop_cycle = plt.rcParams["axes.prop_cycle"]
#     colors = prop_cycle.by_key()["color"]

#     #
#     for index, (model_name, data) in enumerate(engines.items()):
#         # Left plot
#         axes[0].scatter(x=data[x_axis], y=data[y_axis], c="r", s=5)

#         # Right side plot
#         axes[1].scatter(
#             x=data[x_axis],
#             y=data[y_axis],
#             c=colors[index],
#             s=5,
#             label=model_name,
#         )

#         if polynomial_order:
#             coefs = np.polyfit(data[x_axis], data[y_axis], polynomial_order)
#             interpolator = np.poly1d(coefs)

#             _min = data[x_axis].min()
#             _max = data[x_axis].max()

#             axis_interpolater = np.linspace(_min, _max)
#             axes[1].plot(
#                 axis_interpolater,
#                 interpolator(axis_interpolater),
#                 c=colors[index],
#             )


# def plot_all_engines(
#     axes: Tuple[plt.Axes],
#     databank: pd.DataFrame,
#     x_axis: str,
#     y_axis: str,
# ) -> Tuple[plt.Axes]:
#     for ax in axes:
#         ax.scatter(x=databank[x_axis], y=databank[y_axis], c="grey", s=3)
#     return axes


# def main():
#     # init
#     model_name = "PW11"

#     # get ICAO emissions databank
#     gaseous_databank = readers.get_gaseous_databank()

#     # engines of interest
#     model = gaseous_databank[gaseous_databank["model"].str.contains(model_name)]

#     # split engines
#     engines = {
#         "PW1100G - Block A": model[model["model"].str.contains("Block-A")],
#         "PW1100G - Block C": model[model["model"].str.contains("Block-C")],
#         "PW1100G - Block D": model[model["model"].str.contains("Block-D")],
#     }

#     # pivot emissions
#     databank_emissions = extract_emissions(gaseous_databank)

#     engine_emissions = {}
#     for engine_name, engine_data in engines.items():
#         engine_emissions[engine_name] = extract_emissions(engine_data)

#     figures_params = [
#         # OPR = f(rated_thrust)
#         {
#             "x_axis": "rated_thrust",
#             "y_axis": "opr",
#             "xlim": [0, 200],
#             "ylim": [14, 40],
#             "polynomial_order": 1,
#         },
#         # BPR = f(rated_thrust)
#         {
#             "x_axis": "rated_thrust",
#             "y_axis": "bpr",
#             # "xlim": [0, 200],
#             # "ylim": [10, 14],
#             "polynomial_order": 2,
#         },
#         # NOx = f(thrust)
#         {
#             "x_axis": "thrust",
#             "y_axis": "ienox",
#             "xlim": [0, 200],
#             "ylim": [0, 30],
#             # "polynomial_order": 2,
#         },
#         # CO = f(thrust)
#         {
#             "x_axis": "thrust",
#             "y_axis": "ieco",
#             "xlim": [0, 200],
#             "ylim": [0, 50],
#             # "polynomial_order": 2,
#         },
#         # HC = f(thrust)
#         {
#             "x_axis": "thrust",
#             "y_axis": "iehc",
#             "xlim": [0, 200],
#             "ylim": [0, 20],
#             # "polynomial_order": 2,
#         },
#     ]

#     plot_figure(gaseous_databank, engines, figures_params[0])
#     plot_figure(gaseous_databank, engines, figures_params[1])

#     plot_figure(
#         databank_emissions,
#         engine_emissions,
#         figures_params[2],
#     )

#     plot_figure(
#         databank_emissions,
#         engine_emissions,
#         figures_params[3],
#     )

#     plot_figure(
#         databank_emissions,
#         engine_emissions,
#         figures_params[4],
#     )

#     plt.legend()
#     plt.show()


# if __name__ == "__main__":
#     # choose the model to verifi
#     model = MODELS_IDENTIFICATION["PW1100G"]

#     main(model)
