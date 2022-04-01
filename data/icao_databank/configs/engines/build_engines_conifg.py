import glob
import os

import yaml


def main():
    # initialize
    engines_config = {
        "identification": {},
        "remove": [],
        "update": {},
        "validation": {},
    }

    file_extension = "**/**/*.yaml"

    # create the query
    directory = os.path.dirname(__file__)
    searching_query = os.path.join(directory, file_extension)

    for filename in glob.glob(searching_query):
        # load inputs
        with open(filename) as infile:
            inputs = yaml.safe_load(infile)

        engine_identification = inputs["identification"]
        engine_name = list(engine_identification.keys())[0]

        # update engine_configs
        engines_config["identification"].update(inputs["identification"])
        engines_config["remove"].extend(inputs["remove"])
        engines_config["update"].update(inputs["update"])
        engines_config["validation"][engine_name] = inputs["validation"]

    # save
    save_filename = "engines.yaml"
    save_filepath = os.path.join(directory, save_filename)
    with open(save_filepath, "w") as outfile:
        yaml.dump(engines_config, outfile)


if __name__ == "__main__":
    main()
