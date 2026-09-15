# split data into training data so model doesn't "cheat" by having access to full week data set
# access to week 1-50, then predict 51-58
import numpy as np

TEST_WEEKS = 8 # no. of weeks that will be predicted

def split_dataset(series, test_weeks=TEST_WEEKS):
    # 1d num py array is expected input, but can accept list, series, array etc
    series = np.asarray(series)

    if len(series) < test_weeks:
        raise ValueError(f"min of {test_weeks} weeks of data is required")


    # split into train & test via slicing
    train = series[:-test_weeks] # full range of data minus test_weeks
    test = series[-test_weeks:] # last 8 weeks of data

    return train, test 