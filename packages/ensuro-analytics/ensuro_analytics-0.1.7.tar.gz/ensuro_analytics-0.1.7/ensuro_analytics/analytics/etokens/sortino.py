"""
Functions to compute the Sortino ratio.
"""

from typing import Optional

import numpy as np
import pandas as pd

from .. import DAY, today
from . import TimeUnits, risk_free_rate

REQUIRED_COLUMNS = ["returns", "perfect_returns"]


def current_value(
    data: pd.DataFrame,
    full_ur: bool = False,
    time_resolution: str | TimeUnits = "1D",
    **kwargs,
) -> float:
    """
    Function to compute the current Sortino ratio.
    :param data: DataFrame with the eToken returns.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :return: The Sortino ratio.
    """

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    # Check if there are repeated dates
    assert data.index.get_level_values("date").nunique() == len(
        data.index.get_level_values("date")
    ), "There are repeated dates"

    last_date = data.index.get_level_values("date").max()
    rf_rate = risk_free_rate(end_date=last_date, start_date=last_date - 365 * DAY)

    if full_ur:
        col = "perfect_returns"
    else:
        col = "returns"

    data = data[data[col].notnull()]

    if len(data) == 0:
        return np.nan

    # Compute the number of units in one year based on the time resolution
    yearly_units = time_resolution.n_units_in_one_year

    # Compute the reference rate
    ref_r = (1 + rf_rate) ** (1 / yearly_units) - 1

    # Compute the Sortino ratio
    residuals = ref_r - data[data[col] - ref_r < 0][col]
    ddev = np.sqrt((residuals**2).sum() / len(data))
    sortino = (data[col].mean() - ref_r) / ddev

    return sortino


def at_t(
    data: pd.DataFrame,
    date: pd.Timestamp,
    full_ur: bool = False,
    time_resolution: str | TimeUnits = "1D",
    **kwargs,
) -> float:
    """
    Function to compute the Sortino ratio at a given date.
    :param data: DataFrame with the eToken returns.
    :param date: Date at which we want to compute the Sortino ratio.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :return: The Sortino ratio.
    """

    if date.tz is None:
        date = date.tz_localize("UTC")

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    assert date > data.index.get_level_values("date").min() + pd.Timedelta(
        f"{time_resolution.n_days_in_unit}D"
    ), "Date is too early"

    mask = data.index.get_level_values("date") < date

    return current_value(data[mask].copy(), full_ur=full_ur, time_resolution=time_resolution)


def time_series(
    data: pd.DataFrame,
    full_ur: bool = False,
    time_resolution: str | TimeUnits = "1D",
    freq: str = "1W",
    end_date: Optional[pd.Timestamp] = today(),
    start_date: Optional[pd.Timestamp] = today() - 90 * DAY,
    **kwargs,
) -> pd.Series:
    """
    Computes the Sortino ratio time series.
    :param data: DataFrame with the eToken returns.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :param freq: Frequency of the time series.
    :param end_date: Maximum date. If None, the maximum date in the period column is used.
    :param start_date: Minimum date. If None, the minimum date in the period column is used.
    :return: The Sortino ratio time series.
    """

    # Localize the dates as UTC if they are not localized
    if start_date.tz is None:
        start_date = start_date.tz_localize("UTC")

    if end_date.tz is None:
        end_date = end_date.tz_localize("UTC")

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    freq_unit = TimeUnits("1" + freq[-1])
    freq_days = int(freq[:-1]) * freq_unit.n_days_in_unit

    start_date = max(
        start_date,
        data.index.get_level_values("date").min() + pd.Timedelta(f"{freq_days}D"),
        data.index.get_level_values("date").min() + pd.Timedelta(f"{time_resolution.n_days_in_unit}D"),
    )

    ts_dates = pd.date_range(start=start_date, end=end_date, freq=freq, tz="UTC")

    ts = pd.Series(
        index=ts_dates,
        data=[at_t(data, date, full_ur=full_ur, time_resolution=time_resolution) for date in ts_dates],
    )

    return ts
