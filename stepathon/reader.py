import locale
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

locale.setlocale(locale.LC_ALL, "en_AU.UTF-8")


def dataframe_from_csv_path_or_url(string, **kwargs):
    if urlparse(string).scheme in ("http", "https"):
        r = requests.get(string)
        return pd.read_csv(BytesIO(r.content), **kwargs)
    elif Path(string).is_file():
        return pd.read_csv(string, **kwargs)
    else:
        raise RuntimeError


def get_plot_data_dataframe(string):
    if string is None:
        string = r"https://drive.google.com/uc?id=11lotEVAyuIeFY4WXxOgjYqrnDCcUf9ZE"
    return dataframe_from_csv_path_or_url(string, parse_dates=False)


def _clean(x):
    if isinstance(x, str):
        return locale.atoi(x.strip().replace(" ", ""))
    return x


def read_steps(filename):
    """reads excel file and returns steps and group data

    Parameters
    ----------
    filename : _type_
        _description_
    """
    xl_data = pd.read_excel(
        filename,
        index_col=0,
        parse_dates=False,
    )
    group = xl_data.iloc[:, 0]
    steps = xl_data.iloc[:, 1:].fillna(0).applymap(_clean).astype(int).cumsum(axis=1)
    steps.columns = pd.DatetimeIndex(steps.columns)

    return steps, group


def read_excel_url(url):
    r = requests.get(url)
    data = r.content
    return pd.read_csv(BytesIO(data), parse_dates=False)
