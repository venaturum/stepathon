import numpy as np

from stepathon import Map, TimestampedGeoJson


def create_geojson_features(plot_data, highlight=None):
    colours = ["#00A7B8", "#0D2D6C", "#00B480", "#005A65", "#005F9E"]
    group_ids = sorted(plot_data["group"].unique())
    colour_map = dict(zip(group_ids, colours)) if len(group_ids) <= 5 else {}

    if highlight:
        plot_data = plot_data.sort_values("name", key=lambda x: x == highlight)
        if highlight == "team":
            plot_data = plot_data.query("name in @group_ids")

    features = []
    for row in plot_data.itertuples():
        fillcolor = (
            "red" if row.name == highlight else colour_map.get(row.group, "#00A7B8")
        )
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.longitude, row.latitude],
            },
            "properties": {
                "name": row.name,
                "tooltip": f"{row.name}: {int(row.steps):,}",
                "time": row.datetime,
                "style": {"color": ""},
                "icon": "circle",
                "iconstyle": {
                    "fillColor": fillcolor,
                    "fillOpacity": 1,
                    "stroke": "true",
                    "radius": 5,
                },
            },
        }
        features.append(feature)
    return features


def create_map(plot_data, highlight=None):
    geojson_features = create_geojson_features(plot_data, highlight)
    minmax = np.matmul(
        np.array([[1.1, -0.1], [-0.1, 1.1]]),
        plot_data[["latitude", "longitude"]].aggregate([np.min, np.max]).to_numpy(),
    )

    m = Map(location=list(minmax.mean(axis=0)))
    m.fit_bounds([list(minmax[0]), list(minmax[1])])

    TimestampedGeoJson(
        geojson_features,
        period="PT1H",
        duration="PT0H",
        transition_time=10,
        auto_play=True,
    ).add_to(m)
    return m
