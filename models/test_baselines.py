from models.baselines import naive
import numpy as np

def test_naive_repeats_last_value():
    forecast = naive([1, 2, 3, 4, 5], h=3)
    assert list(forecast) == [5, 5, 5]

def test_naive_output_length_matches_h():
    forecast = naive(np.arange(50), h=8)
    assert len(forecast) == 8

def test_naive_returns_numpy_array():
    forecast = naive([1, 2, 3], h=2)
    assert isinstance(forecast, np.ndarray)

def test_empty_train_raises():
    try:
        naive([], h=3)
    except ValueError:
        return
    assert False, "should have raised"

def test_zero_horizon_raises():
    try:
        naive([1, 2, 3], h=0)
    except ValueError:
        return
    assert False, "should have raised"

if __name__ == "__main__":
    test_naive_repeats_last_value()
    test_naive_output_length_matches_h()
    test_naive_returns_numpy_array()
    test_empty_train_raises()
    test_zero_horizon_raises()
    print("all baseline tests pass")