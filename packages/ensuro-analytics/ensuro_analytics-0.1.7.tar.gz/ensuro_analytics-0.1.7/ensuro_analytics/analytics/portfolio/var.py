import gc
import warnings
from typing import Optional

import numpy as np
import pandas as pd

from ensuro_analytics.analytics import DAY, today

from .active_policies import at_t as active_at_
from .active_policies import current_value as active

REQUIRED_COLUMNS = ["payout", "actual_payout", "start", "expiration", "expired_on"]


def _simulation_var_level(
    _data: pd.DataFrame,
    time_window: int,
    time_col: str,
    n_policies: int,
    n_simulation: int,
    level: float | int | list[float] | list[int],
) -> float | list[float]:
    """
    Runs the simulations to compute the VaR at the given level(s).
    """

    dates = pd.date_range(start=_data[time_col].min(), end=_data[time_col].max(), freq="D")

    if time_window >= len(dates):
        dates = dates[-1:]
    else:
        dates = dates[time_window:]

    min_indices = {}
    max_indices = {}

    times = []
    for date in dates:
        tmp = _data[(_data[time_col] >= date - pd.Timedelta(days=time_window)) & (_data[time_col] < date)]
        if tmp.shape[0] > n_policies:
            times.append(date)
            min_indices[date] = tmp.index.min()
            max_indices[date] = tmp.index.max()

    times = np.array(times)

    assert len(times) > 0, "Time window is too narrow"

    # payouts and triggered policies
    payouts = _data.payout.values
    triggered = (_data.actual_payout > 0).values

    # draw which time windows bucket in each simulation
    random_times = times[np.random.choice(len(times), n_simulation, replace=True)]

    # draw which payouts
    random_policies_indices = np.zeros((n_policies, n_simulation), dtype=int)
    for j in range(n_simulation):
        # draw only policies inside the time window bucket
        random_policies_indices[:, j] = np.random.randint(
            min_indices[random_times[j]], max_indices[random_times[j]], n_policies
        )
    random_policies = payouts[random_policies_indices]

    # draw which triggered
    random_triggered_indices = np.zeros((n_policies, n_simulation), dtype=int)
    for j in range(n_simulation):
        # draw only triggers inside the time window bucket
        random_triggered_indices[:, j] = np.random.randint(
            min_indices[random_times[j]], max_indices[random_times[j]], n_policies
        )
    random_triggered = triggered[random_triggered_indices]

    # calculate the loss to exposure
    losses = np.sum(random_policies * random_triggered, axis=0)
    exp = np.sum(random_policies, axis=0)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        loss_to_exposure = losses / exp

    if isinstance(level, list):
        return [np.percentile(loss_to_exposure, l) for l in level]
    else:
        return np.percentile(loss_to_exposure, level)


def current_value(
    data: pd.DataFrame,
    level: Optional[float | int | list[float] | list[int]] = 90.0,
    n_simulation: Optional[int] = 1000,
    time_window: Optional[int] = 30,
    time_col: Optional[str] = "start",
    **kwargs,
) -> float | list[float]:
    """
    Computes the current value at risk (VaR) for the given data at the given level(s).
    Given time_window days and a time_col column, the function draws n_simulation samples of portfolio of sizes all
    equal to the currently active one, with all samples being made of policies that are within time_window days
    from each other. The function then computes the loss to exposure for each sample and returns the level-th
    percentile of the loss to exposure distribution.
    :param data: DataFrame with the data.
    :param level: VaR level(s) to compute.
    :param n_simulation: Number of simulations to run.
    :param time_window: Time window in days.
    :param time_col: Column with the time data.
    :return: VaR at the given level(s).
    """

    # number of policies to use for simulations
    n_policies = active(data)

    assert n_policies > 0, "No currently active policies"

    _data = data.copy()

    # post-mortem
    _data = _data.loc[data.expiration <= today()]

    assert (
        _data.shape[0] > n_policies
    ), "Can not compute VaR with the number of currently active portfolio: not enough historical data"

    # sort
    _data.sort_values(time_col, inplace=True)
    _data[time_col] = pd.to_datetime(_data[time_col].dt.date)
    _data.reset_index(drop=True, inplace=True)

    return _simulation_var_level(_data, time_window, time_col, n_policies, n_simulation, level)


def at_t(
    data: pd.DataFrame,
    date: pd.Timestamp,
    level: Optional[float | int | list[float] | list[int]] = 90.0,
    n_simulation: Optional[int] = 1000,
    time_window: Optional[int] = 30,
    time_col: Optional[str] = "start",
    **kwargs,
) -> float | list[float]:
    """
    Computes the value at risk (VaR) for the given data at the given level(s) at the given date.
    Given time_window days and a time_col column, the function draws n_simulation samples of policies of sizes all
    equal to the ones active at the given date, with all samples being made of portfolio that are within time_window
    days from each other. The function then computes the loss to exposure for each sample and returns the level-th
    percentile of the loss to exposure distribution.
    :param data: DataFrame with the data.
    :param date: Date at which to compute the VaR.
    :param level: VaR level(s) to compute.
    :param n_simulation: Number of simulations to run.
    :param time_window: Time window in days.
    :param time_col: Column with the time data.
    :return: VaR at the given level(s).
    """

    # number of policies to use for simulations
    n_policies = active_at_(data, date)

    assert n_policies > 0, "No active policies at the given date"

    _data = data.copy()

    # post-mortem
    _data = _data.loc[data.expiration <= date]

    assert (
        _data.shape[0] > n_policies
    ), "Can not compute VaR with the number of active portfolio at the given date: not enough historical data"

    # sort
    _data.sort_values(time_col, inplace=True)
    _data[time_col] = pd.to_datetime(_data[time_col].dt.date)
    _data.reset_index(drop=True, inplace=True)

    return _simulation_var_level(_data, time_window, time_col, n_policies, n_simulation, level)


def time_series(
    data: pd.DataFrame,
    freq: str = "1W",
    end_date: Optional[pd.Timestamp] = today(),
    start_date: Optional[pd.Timestamp] = today() - 90 * DAY,
    period_column: str = "expiration",
    level: Optional[float | int | list[float] | list[int]] = 90.0,
    n_simulation: Optional[int] = 1000,
    time_window: Optional[int] = 15,
    time_col: Optional[str] = "start",
    **kwargs,
) -> pd.Series | pd.DataFrame:
    """
    Computes the time series of the value at risk (VaR) for the given data at the given level(s).
    :param data: DataFrame with the data.
    :param freq: Frequency of the time series.
    :param end_date: End date of the time series.
    :param start_date: Start date of the time series.
    :param period_column: Column to consider as the period of the time series.
    :param level: VaR level(s) to compute.
    :param n_simulation: Number of simulations to run.
    :param time_window: Time window in days for the simulations.
    :param time_col: Column from which to draw policies in the simulations.
    :return: VaR time series at the given level(s).
    """

    _data = data.copy()

    # post-mortem
    _data = _data.loc[data.expiration <= today()]

    # sort
    _data.sort_values(time_col, inplace=True)
    _data[time_col] = pd.to_datetime(_data[time_col].dt.date)
    _data.reset_index(drop=True, inplace=True)

    # date index
    dates = pd.date_range(_data[period_column].min(), _data[period_column].max(), freq=freq)

    if isinstance(level, float | int):
        var = np.zeros(len(dates))
        for i, date in enumerate(dates):
            try:
                var[i,] = at_t(_data, date, level, n_simulation, time_window, time_col)
            except:
                var[i,] = np.nan

        var = pd.Series(var, index=dates, name="VaR")

    elif isinstance(level, list):
        var = np.zeros((len(dates), len(level)))
        for i, date in enumerate(dates):
            try:
                var[i,] = at_t(_data, date, level, n_simulation, time_window, time_col)
            except:
                var[i,] = np.nan

        var = pd.DataFrame(var, index=dates, columns=[f"VaR_{l}" for l in level])

    # Filter by start and end date
    if start_date is not None:
        var = var.loc[var.index >= start_date]
    if end_date is not None:
        var = var.loc[var.index <= end_date]

    return var
