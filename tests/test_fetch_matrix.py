import asyncio
from contextlib import nullcontext as does_not_raise
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
from aioresponses import aioresponses

from get_matrix import SOURCE_URL, fetch_matrix, get_matrix
url: str = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"


# Пример корректного тела матрицы
MOCK_MATRIX_TEXT: str = """1  |  2  |  3  |  4
--------------------
5  |  6  |  7  |  8
--------------------
9  |  10 |  11 |  12
--------------------
13 |  14 |  15 |  16"""


@pytest.mark.asyncio
async def test_fetch_matrix_type_str(url=url):
    async with aiohttp.ClientSession() as session:
        result = await fetch_matrix(session,url)
        assert type(result) == str


@pytest.mark.asyncio
async def test_fetch_matrix_success(mock_aiohttp):
    mock_aiohttp.get(SOURCE_URL, status=200, body=MOCK_MATRIX_TEXT)
    async with aiohttp.ClientSession() as session:
        result = await fetch_matrix(session, SOURCE_URL)
    assert '1' in result
    assert '16' in result


@pytest.mark.asyncio
async def test_fetch_matrix_500_error(mock_aiohttp, caplog):
    url: str = "https://example.com/matrix.txt"
    mock_aiohttp.get(url, status=500)
    async with aiohttp.ClientSession() as session:
        with pytest.raises(Exception) as exc_info:
            await fetch_matrix(session, url)

    assert "HTTP 500" in caplog.text


@pytest.mark.asyncio
async def test_fetch_matrix_404_error(mock_aiohttp, caplog):

    mock_aiohttp.get(SOURCE_URL, status=404)
    async with aiohttp.ClientSession() as session:
        with pytest.raises(Exception) as exc_info:
            await fetch_matrix(session, SOURCE_URL)

    assert "HTTP 404" in caplog.text


@pytest.mark.asyncio
async def test_fetch_matrix_server_error(mock_aiohttp, caplog):
    url: str = "https://rawgithubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    # mock_aiohttp.get(url)
    async with aiohttp.ClientSession() as session:
        with pytest.raises(aiohttp.ClientConnectionError):
            await fetch_matrix(session, url)

    # assert "HTTP 404" in caplog.text    

# @pytest.mark.asyncio
# async def test_fetch_matrix_connection_error():
#     session = AsyncMock()
#     session.get.side_effect = ConnectionError("Connection refused")

#     with pytest.raises(ConnectionError, match="Connection refused"):
#         fetch_matrix(session, "https://example.com")        


# @pytest.mark.asyncio
# async def test_fetch_matrix_timeout():
#     session = AsyncMock()
#     session.get.side_effect = asyncio.TimeoutError()

#     with pytest.raises(TimeoutError):
#         await get_matrix( "https://example.com/matrix.txt")