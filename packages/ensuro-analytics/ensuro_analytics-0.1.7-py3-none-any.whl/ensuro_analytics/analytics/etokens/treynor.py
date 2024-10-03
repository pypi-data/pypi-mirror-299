"""
Functions to compute the Treynor.
"""

from typing import Optional

import numpy as np
import pandas as pd

from .. import DAY, today
from . import TimeUnits, beta, get_market_returns, risk_free_rate

REQUIRED_COLUMNS = ["returns", "perfect_returns"]


def current_value(
    data: pd.DataFrame,
    full_ur: bool = False,
    time_resolution: str | TimeUnits = "1D",
    **kwargs,
) -> float:
    """
    Function to compute the current Treynor.
    :param data: DataFrame with the eToken returns.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :return: The Treynor.
    """

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    # Check if there are repeated dates
    assert data.index.get_level_values("date").nunique() == len(
        data.index.get_level_values("date")
    ), "There are repeated dates"

    last_date = data.index.get_level_values("date").max()

    market_data = get_market_returns(dates=data.index.get_level_values("date"))
    rf_rate = risk_free_rate(end_date=last_date, start_date=last_date - 365 * DAY)

    b = beta.current_value(data, full_ur=full_ur, time_resolution=time_resolution)

    if full_ur:
        col = "perfect_returns"
    else:
        col = "returns"

    # Compute the number of units in one year based on the time resolution
    yearly_units = time_resolution.n_units_in_one_year

    # Compute the reference rate
    ref_r = (1 + rf_rate) ** (1 / yearly_units) - 1

    returns_with_benchmarks = (
        pd.merge(market_data[["date", "returns_sp"]], data.reset_index()[["date", col]])
        .dropna()
        .set_index("date")
    )

    returns_with_benchmarks = returns_with_benchmarks[returns_with_benchmarks.notnull()]

    if len(returns_with_benchmarks) == 0:
        return np.nan

    # Compute the mean return
    returns = returns_with_benchmarks[col].mean()

    # Compute treynor
    t = (returns - ref_r) / b

    return t


def at_t(
    data: pd.DataFrame,
    date: pd.Timestamp,
    full_ur: bool = False,
    time_resolution: str | TimeUnits = "1D",
    **kwargs,
) -> float:
    """
    Function to compute the Treynor at a given date.
    :param data: DataFrame with the eToken returns.
    :param date: Date at which we want to compute the temporal weighted yearly return.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :return: The Treynor at the given date.
    """

    if date.tz is None:
        date = date.tz_localize("UTC")

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    assert date > data.index.get_level_values("date").min() + pd.Timedelta(
        f"{time_resolution.n_days_in_unit}D"
    ), "Date is too early"

    mask = data.index.get_level_values("date") < date

    return current_value(data.loc[mask], full_ur=full_ur, time_resolution=time_resolution)


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
    Computes the Treynor.
    :param data: DataFrame with the eToken returns.
    :param full_ur: Boolean to indicate if we want to compute the full UR.
    :param time_resolution: time resolution of the returns’ time series used in the computation.
    :param freq: Frequency of the time series.
    :param end_date: Maximum date. If None, the maximum date in the period column is used.
    :param start_date: Minimum date. If None, the minimum date in the period column is used.
    :return: The Treynor time series.
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
