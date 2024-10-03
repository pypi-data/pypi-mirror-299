"""
Forecasting submodule. The function predict the value of a metric in the future based on historical data.
"""
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class ForecastResult:
    forecasts: np.ndarray

    @property
    def results(self):
        return self.forecasts

    @property
    def average(self):
        return np.nanmean(self.forecasts)

    @property
    def avg(self):
        return self.average

    def distribution(self, bins: Optional[int | list[float]] = 50):
        return np.histogram(self.forecasts, bins=bins)

    def median(self):
        return np.nanmedian(self.forecasts)

    def percentile(self, q: float | list[float]):
        return np.nanpercentile(self.forecasts, q)

    def p(self, q: float | list[float]):
        return self.percentile(q)

    def quantile(self, q: float | list[float]):
        return self.percentile(q)

    def q(self, q: float | list[float]):
        return self.quantile(q)
