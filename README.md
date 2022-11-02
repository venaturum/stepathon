# stepathon

Download test data [here](https://github.com/venaturum/stepathon/raw/main/test_data/stepathon_test_data.xlsx).

## Installation

To install into a virtual environment:

    python -m venv .venv
    .venv/Scripts/activate
    pip install git+https://github.com/venaturum/stepathon.git --upgrade
 
## Usage

In python:

    from stepathon.api import maps_from_coords_and_steps

    maps_from_coords_and_steps(r"./downloads/stepathon_test_data.xlsx", all_maps=True)

This will create a folder of html files.

Type `help(maps_from_coords_and_steps)` for more options.
