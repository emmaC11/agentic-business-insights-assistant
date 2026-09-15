from models.metrics import mae_calc, mape_calc
import math

def test_mae():
    assert mae_calc([3, 0, 5], [4, 2, 6]) == (1 + 2 + 1) / 3

def test_mape_skips_zeros():
    # only weeks 0 and 2 count -> (1/3 + 1/5) / 2 = 0.2666
    result = mape_calc([3, 0, 5], [4, 2, 6])
    assert abs(result - 0.26666666) < 1e-6

def test_mape_all_zero_is_nan():
    assert math.isnan(mape_calc([0, 0, 0], [1, 2, 3]))

def test_length_mismatch_raises():
    try:
        mape_calc([1, 2], [1, 2, 3])
    except ValueError:
        return
    assert False, "should have raised as array length mismatch"

if __name__ == "__main__":
    test_mae()
    test_mape_skips_zeros()
    test_mape_all_zero_is_nan()
    test_length_mismatch_raises()
    print("all metrics tests pass")