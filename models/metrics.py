# scoring funcs - all models depend on these 2 funcs
import numpy as np
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as mape

# mean absolute error
def mae_calc(actual, pred):
    actual = np.asarray(actual)
    pred = np.asarray(pred)

    if len(actual) != len(pred):
        raise ValueError("actual & pred params must be same length")

    error = mae(actual, pred)
    return error

# mean absolute percentage error
def mape_calc(actual, pred):
    actual = np.asarray(actual)
    pred = np.asarray(pred)

    if len(actual) != len(pred):
        raise ValueError("actual & pred params must be same length")
    # need to add handling for 0s, large volume of 0 quant per week in our dataset
    # (actual - pred) / actual - if 0s not handled lead to zero divison exception
    # remove the 0 postion/index from the array

    # assign bool to see if 0
    mask = actual != 0

    # check least 1 true 
    if not mask.any():
        return float("nan")
    return mape(actual[mask], pred[mask])