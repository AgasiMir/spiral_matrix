from contextlib import nullcontext as does_not_raise

import pytest

from get_matrix import fetch_matrix

url: str = (
    "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
)


@pytest.mark.asyncio
async def test_fetch_matrix(url=url):
    result = await fetch_matrix(url)
    assert type(result) == str
