import numpy as np
import pandas as pd


def _lat_long_to_distance(lat1, lat2, long1, long2):

    deg_to_rad = lambda x: np.pi / 180 * x

    # haversine formulat
    lat1 = deg_to_rad(lat1)
    lat2 = deg_to_rad(lat2)
    long1 = deg_to_rad(long1)
    long2 = deg_to_rad(long2)

    return (
        1.609344
        * 3963.0
        * np.arccos(
            (np.sin(lat1) * np.sin(lat2))
            + np.cos(lat1) * np.cos(lat2) * np.cos(long2 - long1)
        )
    )


def _get_distances_from_coords(coords):
    """in kilometres

    Parameters
    ----------
    coords : numpy.ndarray
        _description_

    Returns
    -------
    _type_
        _description_
    """

    distances_between_coords = _lat_long_to_distance(
        lat1=coords[1:, 0],
        lat2=coords[:-1, 0],
        long1=coords[1:, 1],
        long2=coords[:-1, 1],
    )
    distances_between_coords = np.insert(
        distances_between_coords, (0, len(distances_between_coords)), (0, np.Inf)
    )

    return distances_between_coords.cumsum()


def make_participant_coords(coords, steps, steps_per_km, groupby=None):
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
    """
    if groupby is not None:
        steps = pd.concat([steps, steps.groupby(np.array(groupby)).mean()], axis=0)
    steps = steps.transpose().resample("H").interpolate(method="linear").transpose()
    kilometres = steps / steps_per_km
    cumulative_distances = _get_distances_from_coords(coords)

    sample_points = kilometres.to_numpy()
    upper_index = np.searchsorted(cumulative_distances, sample_points, side="right")
    lower_index = upper_index - 1
    fracs = (sample_points - cumulative_distances[lower_index]) / (
        cumulative_distances[upper_index] - cumulative_distances[lower_index]
    )
    coords = np.concatenate([coords, coords[-1:, :]])

    longitudes = coords[lower_index, 1] * (1 - fracs) + coords[upper_index, 1] * fracs
    latitudes = coords[lower_index, 0] * (1 - fracs) + coords[upper_index, 0] * fracs
    return (
        pd.DataFrame(latitudes, index=kilometres.index, columns=kilometres.columns),
        pd.DataFrame(longitudes, index=kilometres.index, columns=kilometres.columns),
        steps,
    )
