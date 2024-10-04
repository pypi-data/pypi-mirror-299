"""Utilities for fitting models to data."""

from __future__ import annotations
from enum import StrEnum

import pandas as pd
from numpy.polynomial.polynomial import Polynomial


class FittingMethods(StrEnum):
    LINEAR = "Linear"
    QUADRATIC = "Quadratic"


def fit_function(serie: pd.Series, method: FittingMethods) -> callable:
    """Fit a function to the serie.

    Parameters
    ----------
    serie : pd.Series
        The serie to fit.
    method : FittingMethods
        The method to fit.

    Returns
    -------
    pd.Series
        The function fitted to the serie.
    """

    match method:
        case FittingMethods.LINEAR | FittingMethods.QUADRATIC:
            degree = 1 if method == FittingMethods.LINEAR else 2
            poly = Polynomial.fit(serie.index.values, serie.values, deg=degree)
            return poly
        case _:
            raise ValueError(f"Method {method} not implemented.")
