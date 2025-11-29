from contextlib import nullcontext as does_not_raise

import pytest

from get_matrix import make_matrix


@pytest.mark.parametrize(
    "data, expected_result, exc",
    [
        ("- | 1 | 2 | - | 3 | 4 | -", [[1, 2], [3, 4]], does_not_raise()),
        ("-|1|2 | - | 3| 4 | -", [[1, 2], [3, 4]], does_not_raise()),
        ("-|1|2|3|-|4|5|6|-|7|8|9|-", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], does_not_raise()),
        ("-|1|2|3|4|-", [[1, 2], [3, 4]], pytest.raises(AssertionError)),
    ],
)
def test_make_matrix(data, expected_result, exc):
    with exc:
        matrix = make_matrix(data)
        assert matrix == expected_result
