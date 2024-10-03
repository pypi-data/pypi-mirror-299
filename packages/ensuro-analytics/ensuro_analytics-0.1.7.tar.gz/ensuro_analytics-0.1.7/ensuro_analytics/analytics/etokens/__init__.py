from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from environs import Env

env = Env()
env.read_env()

API_V2_URL = env.str("API_V2_URL", "https://offchain-v2.ensuro.co/api/")
LPS_URL = env.str("ETOKEN_URL", API_V2_URL + "lpevents/")


@dataclass
class Today:
    """
    Class to handle the current date
    """

    @property
    def date(self):
        return pd.Timestamp("today").normalize()

    @property
    def str(self):
        return self.date.strftime("%Y-%m-%d")

    def back(self, days: int):
        return (self.date - pd.Timedelta(days=days)).date().strftime("%Y-%m-%d")


today = Today()


class TimeUnits:
    """
    Class to handle time units.
    """

    def __init__(self, unit: str):
        assert unit in ["1D", "1W", "1M", "1Y"], "Invalid unit"
        self.unit = unit

    @property
    def n_units_in_one_year(self):
        """
        Returns the number of units in one year.
        """

        match self.unit:
            case "1D":
                return 365
            case "1W":
                return 52.14
            case "1M":
                return 12.17
            case "1Y":
                return 1
            case _:
                return 0

    @property
    def n_days_in_unit(self):
        """
        Returns the number of days in one unit.
        """

        match self.unit:
            case "1D":
                return 1
            case "1W":
                return 7
            case "1M":
                return 30
            case "1Y":
                return 365
            case _:
                return 0

    @property
    def daily_freq(self):
        """
        Returns the number of days in one unit.
        """

        match self.unit:
            case "1D":
                return "1D"
            case "1W":
                return "7D"
            case "1M":
                return "30D"
            case "1Y":
                return "365D"
            case _:
                return "1D"


@lru_cache
def risk_free_rate(
    start_date: str | pd.Timestamp = today.back(365),
    end_date: str | pd.Timestamp = today.str,
):
    """
    Function to get the risk-free rate from treasury bills.
    :param start_date: Start date for the risk-free rate.
    :param end_date: End date for the risk-free rate.
    :return risk_free_rate: The risk-free rate.
    """

    if isinstance(start_date, pd.Timestamp):
        start_date = start_date.strftime("%Y-%m-%d")

    if isinstance(end_date, pd.Timestamp):
        end_date = end_date.strftime("%Y-%m-%d")

    # Download the 3-month treasury bills
    risk_free_rate = yf.download("^IRX", start=start_date, end=end_date)
    risk_free_rate = risk_free_rate.reset_index()["Open"].mean() / 100

    return risk_free_rate


@lru_cache
def get_market_data(
    start_date: str = today.back(3650),
    end_date: str = today.str,
    ticker: str = "^GSPC",
) -> pd.DataFrame:
    """
    Function to get the market data.
    :param start_date: Start date for the market data.
    :param end_date: End date for the market data.
    :return market_data: The market data.
    """

    # Download the S&P500 data
    df = yf.download(ticker, start=start_date, end=end_date).reset_index()
    df["Date"] = df["Date"].dt.tz_localize("UTC").dt.normalize()
    df.rename(columns={"Close": "close", "Date": "date"}, inplace=True)
    df.set_index("date", inplace=True)

    return df[["close"]]


def get_market_returns(
    dates=None,
    ticker: str = "^GSPC",
    start_date: str = None,
    end_date: str = None,
    freq: str = "1W",
) -> pd.DataFrame:
    """
    Function to get the market returns.
    Either dates or (start_date, end_date, freq) must be provided.
    If dates are provided, the market data is matched with the list of dates.
    If start_date, end_date and freq are provided, the market data is matched with the dates generated from the start_date, end_date and freq.
    :param dates: Dates for the market data.
    :param ticker: Ticker for the market data.
    :param start_date: Start date for the market data.
    :param end_date: End date for the market data.
    :param freq: Frequency for the market data.
    :return market_data: The market data.
    """

    market_data = get_market_data(ticker=ticker)

    # Match the market data with the eToken data, in terms of dates
    # In the market data some dates may be missing due to weekends or holidays
    market_data = _match_market_etoken_dates(dates, start_date, end_date, freq, market_data)

    return market_data[["date", "returns_sp"]]


def _match_market_etoken_dates(dates, start_date, end_date, freq, market_data):
    if dates is not None:
        market_dates = pd.Series(dates)
        market_mask = ~market_dates.isin(market_data.index)
        max_shift = 0
        n_shift = market_mask.sum()
        while market_mask.any():
            market_dates.loc[market_mask] = market_dates.loc[market_mask] - pd.Timedelta(days=1)
            market_mask = ~market_dates.isin(market_data.index)
            max_shift += 1
        if max_shift > 0:
            print(f"Shifted {n_shift} market data entries up to {max_shift} days to match the eToken data.")
        market_data = market_data.loc[market_dates]
        market_data["returns_sp"] = market_data["close"].pct_change()
        market_data.index = dates
        market_data.reset_index(inplace=True)

    elif start_date is not None and end_date is not None:
        dates = pd.date_range(start=start_date, end=end_date, freq=freq)
        market_data = market_data.loc[dates]

        market_data["returns_sp"] = market_data["close"].pct_change()
        market_data.reset_index(inplace=True)

    else:
        raise ValueError("Either dates or start_date and end_date must be provided.")
    return market_data


@lru_cache
def market_returns(
    start_date: str = today.back(365),
    end_date: str = today.str,
    time_resolution: str | TimeUnits = "1W",
    ticker: str = "^GSPC",
) -> pd.DataFrame:
    """
    Function to prepare the S&P500 data to be used in the metrics.
    :param start_date: Start date for the S&P500 data.
    :param end_date: End date for the S&P500 data.
    :param time_resolution: Time resolution for the S&P500 data.
    """

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    start_date = (pd.Timestamp(start_date) - pd.Timedelta(days=365)).strftime("%Y-%m-%d")

    # Download the S&P500 data
    sp_df = yf.download(ticker, start=start_date, end=end_date).reset_index()
    sp_df["Date"] = sp_df["Date"].dt.tz_localize("UTC").dt.normalize()
    sp_df.rename(columns={"Close": "close", "Date": "date"}, inplace=True)
    sp_df.set_index("date", inplace=True)

    sp_df = sp_df.resample(time_resolution.daily_freq).agg({"close": "last"})
    sp_df["returns_sp"] = sp_df["close"].pct_change()

    # Drop the last date (may have incomplete data)
    sp_df = sp_df.iloc[:-1]
    sp_df.reset_index(inplace=True)

    return sp_df[["date", "returns_sp"]]


def get_lps():
    """Function to get the LPs data from the API."""

    session = requests.Session()
    lps_list = []
    url = LPS_URL
    while True:
        response = session.get(url)
        lps_list += response.json()["results"]
        if response.json()["next"] is None:
            break
        url = response.json()["next"]

    return pd.json_normalize(lps_list, sep="_")


def blocks_shots_to_token_metrics(
    etoken_blocks: pd.DataFrame, lps_df: pd.DataFrame, etokens_api_query: list[dict]
) -> pd.DataFrame:
    """
    Function to transform the eToken blocks shots and the LPs data into a DataFrame with daily resolution and all the necessary columns.
    :param etoken_blocks: DataFrame with the eToken blocks shots.
    :param lps_df: DataFrame with the LPs data.
    """

    # Transform the eToken blocks shots columns with correct types
    etoken_blocks["total_supply"] = etoken_blocks.total_supply.astype(float)
    etoken_blocks["scr"] = etoken_blocks.scr.astype(float)
    etoken_blocks["date"] = pd.to_datetime(etoken_blocks["date"], utc=True).dt.normalize()

    # Transform the LPs data columns with correct types
    lps_df.event_tx_timestamp = pd.to_datetime(lps_df.event_tx_timestamp)
    lps_df["date"] = lps_df.event_tx_timestamp.dt.normalize()

    # Compute the deposits and withdrawals
    lps_df["deposit"] = (lps_df.event_type == "deposit").astype(int) * lps_df.amount.astype(float)
    lps_df["withdraw"] = (lps_df.event_type == "withdraw").astype(int) * lps_df.amount.astype(float)

    # Get the eToken address and the eToken URL
    etokens_url_address_map = {r["url"]: r["address"] for r in etokens_api_query}

    # Transform the eToken URL to the eToken address
    lps_df["e_token"] = lps_df.e_token.map(etokens_url_address_map)

    # Compute the daily token balance
    daily_token_balance = (
        etoken_blocks.sort_values(["e_token", "date"])
        .groupby(["e_token", "date"])
        .agg(
            {
                "total_supply": "last",
                "scr": "last",
            }
        )
    )

    # Set a multiindex from the eToken address and the date
    e_tokens = daily_token_balance.reset_index().e_token.unique()
    dates = daily_token_balance.reset_index().date.unique()

    # Don't consider the very last date (may have incomplete data)
    dates = pd.date_range(start=dates.min(), end=dates.max(), freq="D")[:-1]

    # Set the multiindex
    reindex = pd.MultiIndex.from_product([e_tokens, dates], names=["e_token", "date"])
    daily_token_balance = daily_token_balance.reindex(reindex)

    # Fill the missing values of total supply and SCR with the last available value
    daily_token_balance = daily_token_balance.groupby(level="e_token").transform(lambda x: x.bfill().ffill())

    # Compute daily deposits and withdrawals and fill the missing values with 0
    daily_token_balance["deposit"] = lps_df.groupby(["e_token", "date"]).deposit.sum()
    daily_token_balance["withdraw"] = lps_df.groupby(["e_token", "date"]).withdraw.sum()
    daily_token_balance[["withdraw", "deposit"]] = daily_token_balance[["withdraw", "deposit"]].fillna(0)

    # Compute dividends; The dividends are computed as the difference between the total supply of the eToken
    # at time t+1 and t, minus the deposits and plus the withdrawals.
    daily_token_balance["dividend"] = (
        daily_token_balance.groupby(level="e_token").total_supply.diff()
        - daily_token_balance.deposit
        + daily_token_balance.withdraw
    )

    return daily_token_balance


def returns_dataframe(etokens_data: pd.DataFrame, time_resolution: str = "1D") -> pd.DataFrame:
    """
    Computes the dataframe of returns, utilization rate, flow, outlay, and proceeds for each eToken (both nominal and perfect).
    :param etokens_data: Dataframe with eTokens' total supply, deposits, withdrawals, scr, and dividends.
    :param time_resolution: Time resolution for the returns.
    """

    if isinstance(time_resolution, str):
        time_resolution = TimeUnits(time_resolution)

    _aggregation_funcs = {
        "total_supply": "last",
        "scr": "last",
        "dividend": "sum",
        "deposit": "sum",
    }

    # Resample with desired time resolution
    returns = (
        etokens_data.reset_index(level="e_token")
        .groupby("e_token")
        .resample(time_resolution.daily_freq)
        .agg(_aggregation_funcs)
    )

    # Compute the returns
    returns["returns"] = (
        returns["dividend"] / returns.groupby(level="e_token").total_supply.shift()
    ).replace(np.inf, np.nan)
    returns["perfect_returns"] = (
        returns["dividend"] / returns.groupby(level="e_token").scr.shift()
    ).replace(np.inf, np.nan)

    # Compute the utilization rate
    returns["UR"] = returns[f"scr"] / returns["total_supply"]

    # Compute the flow
    returns["flow"] = returns["total_supply"].groupby(level="e_token").diff(1) - returns["dividend"]
    returns["perfect_flow"] = returns["scr"].groupby(level="e_token").diff(1)

    # Fill the first occurrence with the total supply (or SCR)
    first_occurrences = returns.groupby(level="e_token").cumcount() == 0
    returns.loc[first_occurrences, "flow"] = returns.loc[first_occurrences, "total_supply"]
    returns.loc[first_occurrences, "perfect_flow"] = returns.loc[first_occurrences, "scr"]

    # Compute the cumulative flow
    returns["cumflow"] = returns["flow"].cumsum()
    returns["perfect_cumflow"] = returns["perfect_flow"].cumsum()

    # Compute the outlay and proceeds
    returns["outlay"] = returns["flow"].apply(lambda x: 0 if x < 0 else x)
    returns["proceeds"] = -returns["flow"].apply(lambda x: 0 if x > 0 else x)
    returns["perfect_outlay"] = returns["perfect_flow"].apply(lambda x: 0 if x < 0 else x)
    returns["perfect_proceeds"] = -returns["perfect_flow"].apply(lambda x: 0 if x > 0 else x)

    # Drop the last aggregate date (may have incomplete data)
    dates = returns.index.levels[1]
    returns = returns.loc[(slice(None), dates[:-1]), :]

    # Clean the index

    return returns


def filter_first_nonzero(group: pd.DataFrame, column="deposit") -> pd.DataFrame:
    """
    Function to filter the first occurrence of a column with a nonzero value.
    :param group: DataFrame group.
    :param column: Column to filter.
    """
    nonzero_index = group.reset_index()[column].ne(0).idxmax() + 1

    return group.iloc[nonzero_index:]


def filter_returns_dataframe(returns: pd.DataFrame, filter_method="first_deposit"):
    if filter_method == "first_deposit":
        # Start the time series only after the first deposit
        returns = (
            returns.groupby(level="e_token").apply(filter_first_nonzero).reset_index(level=0, drop=True)
        )
    else:
        raise ValueError(f"Filter method {filter_method} not implemented")

    return returns
