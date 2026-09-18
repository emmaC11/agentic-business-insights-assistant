# forecasts / predicts using different models
# every forecasting func follows the same signature
# h-> horizon - number of weeks want to forecast
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
    """next week = average of the last 4 weeks"""

    train = np.asarray(train)

    if len(train) == 0:
        raise ValueError("train np array empty")

    if h <= 0:
        raise ValueError("number of weeks to forecast / horizon must be greater than 0")

    return np.full(h,train[-4:].mean())
