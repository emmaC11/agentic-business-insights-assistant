# forecasts / predicts using different models
# every forecasting func follows the same signature
# h-> horizon - number of weeks want to forecast
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

def naive(train: np.ndarray, h: int) -> np.ndarray:
    """forecast next n weeks, next week = last week"""

    train = np.asarray(train)

    if len(train) == 0:
        raise ValueError("train np array empty")

    if h <= 0:
        raise ValueError("number of weeks to forecast / horizon must be greater than 0")

    # n weeks will be last element of train array
    return np.full(h, train[-1])

def moving_average(train: np.ndarray, h:int) -> np.ndarray:
    """forecast next h weeks using Holt's liner method (double exponential smoothing)
        """

    train = np.asarray(train)

    if len(train) == 0:
        raise ValueError("train np array empty")

    if h <= 0:
        raise ValueError("number of weeks to forecast / horizon must be greater than 0")

    return np.full(h,train[-4:].mean())

def ets(train: np.ndarray, h:int) -> np.ndarray:

    """weighted average of all past weeks, recent weeks count more"""
    train = np.asarray(train)
    
    if len(train) == 0:
        raise ValueError("train np array empty")
    
    if h <= 0:
        raise ValueError("number of weeks to forecast / horizon must be greater than 0")

    model = ExponentialSmoothing (
        train,
        trend="add", # data has upward & downward trend, it can vary per week
        seasonal=None, # have not worked / added seasonal trends
        initialization_method="estimated"
        ).fit()

    forecast = model.forecast(h)

    # remove any negative falues
    forecast = np.clip(forecast, 0, None)

    return np.asarray(forecast)

