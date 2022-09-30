# user inputs coordinates csv, step data -> map(s) produced
# user inputs coordinates csv, step data -> plot_data produced
# user inputs plot data csv -> map(s) produced


# coordinates csv options: --default_url --coord_path --coord_url
# plot_data csv options: --default_url --plot_data_path --plot_data_url
# step_data csv options: --default_url --step_data_path --step_data_url

import pathlib

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from stepathon.map import create_map
from stepathon.plot_data import default_coords, make_plot_data
from stepathon.reader import get_plot_data_dataframe, read_steps


def _make_index(output_directory, persons):
    file_loader = FileSystemLoader(r"C:\Users\rclement\Documents\stepathon\stepathon")
    env = Environment(loader=file_loader)
    template = env.get_template("index_template.html")
    output = template.render(persons=persons)
    with open(output_directory + "/_index.html", "w") as f:
        f.write(output)


def _ensure_directory(output_directory):
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)


def _create_maps(plot_data, all_maps, output_directory):
    _ensure_directory(output_directory)
    if all_maps:
        persons = []
        for name in sorted(plot_data["name"].unique()):
            m = create_map(plot_data, highlight=name)
            m.save(output_directory + f"/{name.replace(' ', '')}.html")
            persons.append({"name": name, "url": f"./{name.replace(' ', '')}.html"})
        _make_index(output_directory, persons)
    else:
        m = create_map(plot_data, highlight=None)
        m.save(output_directory + "/all.html")


def maps_from_plot_data(plot_data_csv, all_maps=False, output_directory="./maps"):
    plot_data = get_plot_data_dataframe(plot_data_csv)
    _create_maps(plot_data, all_maps, output_directory)


def maps_from_coords_and_steps(
    step_data_xlsx,
    coords_csv=None,
    all_maps=False,
    output_directory="./maps",
    steps_per_km=472500 / 363,
):
    """Will create a folder of html files

    Parameters
    ----------
    step_data_xlsx : str
        Path to step data excel document.  The columns should be Name, Group, followed
        by an arbitary number of timestamps, eg "22/09/2022".
    coords_csv : str, optional
        Path to csv.  Csv should have two columns only - no index, no header.
        First column is latitude, second column is longitude.  Coordinates trace the path to be "walked".
        If not supplied then default path coordinates will be used.
    all_maps : bool, optional
        Indicates whether to produce a map per individual participating, or simply
        a single map. By default False
    output_directory : str, optional
        Path to where the html files should be stored, by default "./maps"
    """
    steps, group = read_steps(step_data_xlsx)
    if coords_csv is None:
        coords = default_coords().to_numpy()
    else:
        coords = pd.read_csv(coords_csv, header=None).to_numpy()
    plot_data = make_plot_data(coords, steps, steps_per_km, groupby=group)
    _create_maps(plot_data, all_maps, output_directory)


def plot_data_from_coords_and_steps(coords_csv, step_data, outfile_name):
    pass
