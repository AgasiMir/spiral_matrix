from contextlib import nullcontext as does_not_raise

import pytest

from get_matrix import spiral_counter_clockwise


@pytest.mark.parametrize(
    "list, expected_result, exc",
    [
        ([[1, 2], [3, 4]], [1, 3, 4, 2], does_not_raise()),
        ([[1, 2, 3], [5, 6, 7], [8, 9, 10]], [1, 5, 8, 9, 10, 7, 3, 2, 6], does_not_raise()),
        ([[1, 2]], [1, 2], does_not_raise()),
        ([[]], [], does_not_raise()),
        (None, [], does_not_raise()),
        ([[1, 2, 3], [4, 5, 6]], [1, 4, 5, 6, 2, 3], pytest.raises(AssertionError)),
        ([[1, 2, 3], [4, 5, 6]], [1, 6, 3, 4, 2, 5], pytest.raises(AssertionError)),
    ],
)
def test_spiral_counter_clockwise(list, expected_result, exc):
    with exc:
        result = spiral_counter_clockwise(list)
        assert result == expected_result
