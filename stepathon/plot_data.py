import pandas as pd

from stepathon.distance_data import make_participant_coords


def default_coords():
    from pathlib import Path

    import pandas as pd

    coords = pd.read_csv(Path(__file__).parent / "coords.csv")
    coords.columns = ["long1", "lat1"]
    return coords


def make_plot_data(coords, steps, steps_per_km, groupby=None):
    """_summary_

    Parameters
    ----------
    coords : 2d numpy array
        First column "latitude", second column "longitude"
    steps : pandas.DataFrame
        Indexed by participant, first column a groupby label (eg team, or target destination).
        Rest of columns are a datetime index
    steps_per_km : float
        How many steps in a kilometre?  Used for converting steps to distances.
        Note this doesn't have to be realistic.

    Returns
    ----------
    pandas.Dataframe
    """
    latitudes, longitudes, interpolated_steps = make_participant_coords(
        coords, steps, steps_per_km, groupby
    )
    tidy_data = pd.concat(
        [
            latitudes.melt(
                ignore_index=False, var_name="datetime", value_name="latitude"
            ).set_index("datetime", append=True),
            longitudes.melt(
                ignore_index=False, var_name="datetime", value_name="longitude"
            ).set_index("datetime", append=True),
            interpolated_steps.melt(
                ignore_index=False, var_name="datetime", value_name="steps"
            ).set_index("datetime", append=True),
        ],
        axis=1,
    ).reset_index()
    tidy_data.columns = ["name", "datetime", "latitude", "longitude", "steps"]
    if groupby is not None:
        tidy_data["group"] = tidy_data["name"].map(groupby).fillna(tidy_data["name"])

    return tidy_data


def write_plot_data(filename, coords, steps, steps_per_km, groupby=None):
    """writes csv

    Parameters
    ----------
    coords : 2d numpy array
        First column "latitude", second column "longitude"
    steps : pandas.DataFrame
        Indexed by participant, first column a groupby label (eg team, or target destination).
        Rest of columns are a datetime index
    steps_per_km : float
        How many steps in a kilometre?  Used for converting steps to distances.
        Note this doesn't have to be realistic.
    """
    tidy_data = make_plot_data(coords, steps, steps_per_km, groupby)
    tidy_data.to_csv(filename, index=False)
