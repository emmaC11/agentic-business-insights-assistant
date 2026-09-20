import numpy as np

CROSTON_ALPHA = 0.1

def croston(train: np.ndarray, h: int) -> np.ndarray:
    """croston strong model choice for dataset with lots of 0s, designed specifically for items w intermittent demand""" 
    # used claude to help understand logic required & build fn - as not leveraging library

    train = np.asarray(train)
    # split series into 2, non-zeros & intervals
    non_zeros_indices = np.where(train > 0)[0]
    non_zeros = train[non_zeros_indices]

    # list of gaps in weeks between non zero values
    extended_indices = np.insert(non_zeros, 0, -1)
    intervals = np.diff(extended_indices)

    # used claude for this block below - line 17-25
    size_hat = non_zeros[0]
    interval_hat = intervals[0]

    for size, interval in zip(non_zeros[1:], intervals[1:]):
        size_hat = CROSTON_ALPHA * size + (1 - CROSTON_ALPHA) * size_hat
        interval_hat = CROSTON_ALPHA * interval + (1 - CROSTON_ALPHA) * interval_hat

    # SBA bias correction (Syntetos & Boylan 2005)
    forecast = (size_hat / interval_hat) * (1 - CROSTON_ALPHA / 2)