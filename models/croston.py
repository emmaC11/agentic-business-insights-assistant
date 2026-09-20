import numpy as np

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