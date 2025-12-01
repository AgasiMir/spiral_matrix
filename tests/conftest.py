import pytest
from aioresponses import aioresponses


@pytest.fixture
def mock_aiohttp():
    with aioresponses() as m:
        yield m
