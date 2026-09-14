# scoring funcs - all models depend on these 2 funcs
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as mape

# mean absolute error
def mae_calc(actual: list, pred: list):
    error = mae(actual, pred)
    # print(f"mean absolute error -> {error}")
    return error

# mean absolute percentage error
def mape_calc(actual: list, pred: list):
    error  = mape(actual, pred)
    # print(f"mean absolute percentage error -> {error}")
    return error
