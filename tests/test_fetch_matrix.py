import asyncio
from contextlib import nullcontext as does_not_raise
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
from aioresponses import aioresponses

from get_matrix import SOURCE_URL, fetch_matrix, get_matrix

# Пример корректного тела матрицы
MOCK_MATRIX_TEXT: str = """1  |  2  |  3  |  4
--------------------
5  |  6  |  7  |  8
--------------------
9  |  10 |  11 |  12
--------------------
13 |  14 |  15 |  16"""


@pytest.mark.asyncio
async def test_fetch_matrix_type_str(url=SOURCE_URL):
    async with aiohttp.ClientSession() as session:
        result = await fetch_matrix(session,url)
        assert type(result) == str


@pytest.mark.asyncio
async def test_fetch_matrix_success():
    with aioresponses() as m:
        m.get(SOURCE_URL, status=200, body=MOCK_MATRIX_TEXT)
        async with aiohttp.ClientSession() as session:
            result = await fetch_matrix(session, SOURCE_URL)
        assert '1' in result
        assert '16' in result


# @pytest.mark.asyncio
# async def test_fetch_matrix_500_error():
#     url = "https://example.com/matrix.txt"
#     with aioresponses() as m:
#         m.get(url, status=500)
#         async with aiohttp.ClientSession() as session:
#             with pytest.raises(Exception) as exc_info:
#                 await fetch_matrix(session, url)
#     # assert "HTTP 500" in str(exc_info.value)
#     print(str(exc_info.value))



# @pytest.mark.asyncio
# async def test_fetch_matrix_404_error():
#     with aioresponses() as m:
#         m.get(SOURCE_URL, status=404)
#         async with aiohttp.ClientSession() as session:
#             with pytest.raises(Exception) as exc_info:
#                 await fetch_matrix(session, SOURCE_URL)
#         assert "HTTP 404" in str(exc_info.value)

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