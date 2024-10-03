"""
Portfolio review
"""

import warnings
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from ensuro_analytics.analytics import DAY, today
from ensuro_analytics.analytics.dataframe import create_ensuro_accessors


def _get_var(x: pd.DataFrame, level: float | int | list[float] | list[int], **kwargs) -> float | list[float]:
    if isinstance(level, float | int):
        level = [level]
    try:
        return x.var.current_value(level=level, **kwargs)
    except:
        return [np.nan] * len(level)


def compute_adjusted_target_loss_ratio(
    data: pd.DataFrame,
    target_loss_ratio: float,
    tau_1: float = 30 * 3,
    tau_2: float = 30 * 3,
    lower_bound: float = 0.0,
    upper_bound: float = 1.0,
    pct_trend: float = 1.0,
    consider_active_policies: bool = True,
) -> tuple[float, float]:
    """
    Compute the adjusted target loss ratio.

    Parameters
    ----------
    data : pd.DataFrame
        The data containing the portfolio.
    target_loss_ratio : float
        The target loss ratio.
    tau_1 : float, optional
        The time period for computing the historical surplus and loss-to-exposure, by default 90 days.
    tau_2 : float, optional
        The time period for computing the expected exposure, by default 90 days. This is the period over which
        the deficit is expected to be recovered.
    lower_bound : float, optional
        The lower bound for the adjusted target loss to exposure ratio, by default 0.5.
    upper_bound : float, optional
        The upper bound for the adjusted target loss to exposure ratio, by default 0.95.
    pct_trend : float, optional
        The percentage trend for the expected exposure, by default 1.0.
    consider_active_policies : bool, optional
        Whether to consider active policies in the computation, by default True.

    Returns
    -------
    trget_loss_to_exposure, target_loss_ratio
        The adjusted target loss to exposure ratio and the adjusted target loss ratio.
    """
    # Create the ensuro accessors
    create_ensuro_accessors()

    # Compute the surplus over the last tau_1 days
    mask = (data.expiration < today()) & (data.expiration >= today() - tau_1 * DAY)
    historical_loss_to_exposure = data.loc[mask].loss_to_exposure.current_value(post_mortem=True) / 100
    # Compute the surplus
    historical_surplus = data.loc[mask, "pure_premium"].sum() - data.loc[mask, "actual_payout"].sum()

    if consider_active_policies:
        # Estimate the surplus for the active policies
        historical_surplus += (
            data.loc[data.expired_on.isna(), "pure_premium"].sum()
            - data.loc[data.expired_on.isna(), "payout"].sum() * historical_loss_to_exposure
        )

    target_loss_to_exposure = historical_loss_to_exposure / target_loss_ratio

    if historical_surplus >= 0:
        # If the performance is positive, simply return the target loss ratio
        return target_loss_to_exposure * 100, target_loss_ratio * 100

    else:
        historical_surplus *= -1

    # Compute the expected exposure that will be received in the next tau_2 days;
    # at the moment, this is set = the pure premium of the last tau_2 days
    mask = data.start >= today() - tau_2 * DAY
    expected_exposure = data.loc[mask, "payout"].sum() * pct_trend

    # We want the pure premium collected with the next tau_2 days to be enough to cover:
    # 1. the expected loss +
    # 2. the historical surplus lost in the last tau_1 days

    target_loss_to_exposure = (
        historical_loss_to_exposure / target_loss_ratio
    )  # This is the target loss to exposure
    # ratio without the deficit
    extra_loss_to_exposure = (
        historical_surplus / expected_exposure
    )  # This is the extra loss to exposure ratio

    # The target loss to exposure ratio is adjusted by the extra loss to exposure ratio
    adjusted_target_loss_to_exposure = target_loss_to_exposure + extra_loss_to_exposure

    # Bound between lower_bound and upper_bound
    adjusted_target_loss_to_exposure = np.clip(adjusted_target_loss_to_exposure, lower_bound, upper_bound)

    # Compute the adjusted target loss ratio
    adjusted_target_loss_ratio = historical_loss_to_exposure / adjusted_target_loss_to_exposure

    return adjusted_target_loss_to_exposure * 100, adjusted_target_loss_ratio * 100


@dataclass
class PortfolioReview:
    """
    A class used to review a portfolio of insurance policies.

    ...

    Attributes
    ----------
    data : pd.DataFrame
        a pandas DataFrame containing the policies data
    split_on : list[str]
        a list of columns to split the portfolio on

    Methods
    -------
    from_data(data: pd.DataFrame, split_on: str | list[str] = ["rm_name"]) -> "PortfolioReview":
        Creates a PortfolioReview object from a dataframe.
    _validate_data(data: pd.DataFrame, cols: Optional[list[str]] = None):
        Validates the data
    review(show_first_date: bool = True, show_predicted_loss_to_exposure: bool = True, show_current_portfolio_pct: bool = True, **kwargs) -> "_CompiledReview":
        Computes the portfolio review
    """

    data: pd.DataFrame
    split_on: list[str]

    @classmethod
    def from_data(
        cls,
        data: pd.DataFrame,
        split_on: str | list[str] = ["rm_name"],
        validate_columns: Optional[list[str]] = None,
    ) -> "PortfolioReview":
        """
        Creates a PortfolioReview object from a dataframe.

        Parameters
        ----------
        data : pd.DataFrame
            policies dataframe
        split_on : str | list[str]
            list of columns to split the portfolio on
        validate_columns : Optional[list[str]]
            list of columns that the data should have; standard portfolio columns are validated by default.

        Returns
        -------
        PortfolioReview
            a PortfolioReview object
        """

        cls._validate_data(data, cols=validate_columns)
        if isinstance(split_on, str):
            split_on = [split_on]

        create_ensuro_accessors()

        return cls(
            data=data,
            split_on=split_on,
        )

    @staticmethod
    def _validate_data(data: pd.DataFrame, cols: Optional[list[str]] = None):
        """
        Validates the data

        Parameters
        ----------
        data : pd.DataFrame
            policies dataframe
        cols : Optional[list[str]]
            list of columns to validate
        """
        assert "expired_on" in data.columns, "expired_on column is required"
        assert "start" in data.columns, "start column is required"
        assert "expiration" in data.columns, "expiration column is required"
        assert "pure_premium" in data.columns, "pure_premium column is required"
        assert "payout" in data.columns, "payout column is required"
        assert "actual_payout" in data.columns, "actual_payout column is required"

        if cols is not None:
            for col in cols:
                assert col in data.columns, f"{col} column is required"

    def review(
        self,
        show_first_date: bool = True,
        show_predicted_loss_to_exposure: bool = True,
        show_current_portfolio_pct: bool = True,
        average_duration: Optional[str] = None,
        var_levels: Optional[float | int | list[float] | list[int]] = None,
        **kwargs,
    ) -> "_CompiledReview":
        """
        Computes the portfolio review

        Parameters
        ----------
        show_first_date : bool
            whether to show the first date in the review
        show_predicted_loss_to_exposure : bool
            whether to show the predicted loss to exposure in the review
        show_current_portfolio_pct : bool
            whether to show the current portfolio percentage in the review
        average_duration : Optional[str]
            If "expected", the expected average duration is shown. If "actual", the actual average duration is shown. If None, the average duration is not shown.
        var_levels : Optional[float | list[float]]
            VaR levels to compute
        **kwargs
            arbitrary keyword arguments

        Returns
        -------
        _CompiledReview
            a compiled review object
        """

        columns = [
            "first_date",
            "pred_loss_to_exposure",
            "loss_to_exposure",
            "loss_ratio",
            "volume",
            "current_pct",
            "average_duration",
            "target-loss-to-exposure",
            "target-loss-ratio",
        ]

        if average_duration is not None:
            if average_duration not in ["expected", "actual"]:
                raise ValueError("average_duration should be 'expected', 'actual', or None")
            elif average_duration == "expected":
                self.data["duration"] = (self.data.expiration - self.data.start).dt.days
            elif average_duration == "actual":
                self.data["duration"] = (self.data.expired_on - self.data.start).dt.days

        if show_current_portfolio_pct is True:
            total_exposure = self.data.exposure.current_value()

        grouped_data = self.data.groupby(self.split_on)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            result = {
                "loss_to_exposure": grouped_data.apply(
                    lambda x: x.loss_to_exposure.current_value(post_mortem=True)
                ),
                "loss_ratio": grouped_data.apply(lambda x: x.loss_ratio.current_value(post_mortem=True)),
                "volume": grouped_data.apply(lambda x: (x.expiration <= today()).sum()),
            }
        if show_first_date is True:
            result["first_date"] = grouped_data.start.min().dt.date
        else:
            columns.remove("first_date")

        if show_current_portfolio_pct is True:
            result["current_pct"] = (
                grouped_data.apply(lambda x: x.exposure.current_value()) / total_exposure * 100
            )
        else:
            columns.remove("current_pct")

        if show_predicted_loss_to_exposure is True:
            result["pred_loss_to_exposure"] = grouped_data.apply(
                lambda x: x.pure_premium.sum() / x.payout.sum() * 100
            )
        else:
            columns.remove("pred_loss_to_exposure")

        if average_duration is not None:
            result["average_duration"] = grouped_data.duration.mean()
        else:
            columns.remove("average_duration")

        if "target_loss_ratio" in kwargs:
            target_lr_lte = grouped_data.apply(
                lambda x: pd.Series(compute_adjusted_target_loss_ratio(x, **kwargs["target_loss_ratio"]))
            )
            result["target-loss-to-exposure"] = target_lr_lte[0]
            result["target-loss-ratio"] = target_lr_lte[1]

        else:
            columns.remove("target-loss-to-exposure")
            columns.remove("target-loss-ratio")

        if var_levels is not None:
            if isinstance(var_levels, float | int):
                var_levels = [var_levels]
            var_df = grouped_data.apply(lambda x: pd.Series(_get_var(x, var_levels, **kwargs)) * 100)
            for i, l in enumerate(var_levels):
                result[f"VaR_{l}"] = var_df[i]
                columns.append(f"VaR_{l}")

        # Put the results in a single dataframe
        results = pd.DataFrame(result)[columns]
        results.sort_index(inplace=True)

        return _CompiledReview(results)


@dataclass
class _CompiledReview:
    """
    A class used to compile and represent the results of a portfolio review.

    ...

    Attributes
    ----------
    portfolio_review : pd.DataFrame
        a pandas DataFrame containing the results of the portfolio review

    Methods
    -------
    to_df() -> pd.DataFrame:
        Returns a copy of the portfolio review results as a pandas DataFrame.
    to_string(**kwargs) -> str:
        Returns a string representation of the portfolio review results.
    print(**kwargs) -> None:
        Prints the string representation of the portfolio review results.
    """

    portfolio_review: pd.DataFrame

    def to_df(self) -> pd.DataFrame:
        """
        Returns a copy of the portfolio review results as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            a copy of the portfolio review results
        """

        return self.portfolio_review.copy()

    def to_string(self, **kwargs) -> str:
        """
        Returns a string representation of the portfolio review results.

        Parameters
        ----------
        **kwargs
            arbitrary keyword arguments

        Returns
        -------
        str
            a string representation of the portfolio review results
        """

        return self.portfolio_review.to_string(float_format="{:,.2f}%".format, **kwargs)

    def print(self, **kwargs) -> None:
        """
        Prints the string representation of the portfolio review results.

        Parameters
        ----------
        **kwargs
            arbitrary keyword arguments
        """

        print(self.to_string(**kwargs))
