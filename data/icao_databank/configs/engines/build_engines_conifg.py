import glob
import os

import yaml


def main():
    # initialize
    engines_config = {"remove": [], "update": {}}

    file_extension = "**/**/*.yaml"

    # create the query
    directory = os.path.dirname(__file__)
    searching_query = os.path.join(directory, file_extension)

    for filename in glob.glob(searching_query):
        # load inputs
        with open(filename) as infile:
            inputs = yaml.safe_load(infile)

        # update engine_configs
        engines_config["remove"].extend(inputs["remove"])
        engines_config["update"].update(inputs["update"])

    # save
    save_filename = "engines.yaml"
    save_filepath = os.path.join(directory, save_filename)
    with open(save_filepath, "w") as outfile:
        yaml.dump(engines_config, outfile)


if __name__ == "__main__":
    main()
