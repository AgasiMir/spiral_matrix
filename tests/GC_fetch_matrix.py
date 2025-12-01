import pytest
import aiohttp
import asyncio

from get_matrix import fetch_matrix

def fake_retry(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

# @pytest.mark.asyncio
# async def test_fetch_matrix_success(mock_aiohttp):
#     url = "http://example.com/matrix"
#     mock_response_text = "1 2 3\n4 5 6\n7 8 9"

#     mock_aiohttp.get(url, status=200, body=mock_response_text)

#     async with aiohttp.ClientSession() as session:
#         result = await fetch_matrix(session, url)

#     assert result == mock_response_text


# @pytest.mark.asyncio
# async def test_fetch_matrix_http_error(mock_aiohttp, caplog):
#     url = "http://example.com/matrix"
#     mock_aiohttp.get(url, status=404, body="Not Found")

#     async with aiohttp.ClientSession() as session:
#         with pytest.raises(aiohttp.ClientResponseError):
#             await fetch_matrix(session, url)

#     assert "Ошибка HTTP 404" in caplog.text


@pytest.mark.asyncio
async def test_fetch_matrix_timeout_error(mock_aiohttp, caplog, monkeypatch):
    monkeypatch.setattr("get_matrix.retry", fake_retry)
    url = "http://example.com/matrix"
    mock_aiohttp.get(url, exception=asyncio.TimeoutError())

    async with aiohttp.ClientSession() as session:
        with pytest.raises(asyncio.TimeoutError):
            await fetch_matrix(session, url)

    assert "Таймаут при запросе" in caplog.text


# @pytest.mark.asyncio
# async def test_fetch_matrix_payload_error(mock_aiohttp, caplog):
#     url = "http://example.com/matrix"
#     mock_aiohttp.get(url, exception=aiohttp.ClientPayloadError())

#     async with aiohttp.ClientSession() as session:
#         with pytest.raises(aiohttp.ClientPayloadError):
#             await fetch_matrix(session, url)

#     assert "Ошибка чтения данных" in caplog.text











# @pytest.mark.asyncio
# async def test_fetch_matrix_empty_response(mock_aiohttp, caplog):
#     url = "http://example.com/matrix"
#     # Важно: fetch_matrix не проверяет пустоту — это делает get_matrix
#     # Значит, fetch_matrix должна вернуть пустую строку без ошибки
#     mock_aiohttp.get(url, status=200, body="")

#     async with aiohttp.ClientSession() as session:
#         result = await fetch_matrix(session, url)

#     assert result == ""
#     # assert "Успешно загружены данные, размер: 0" in caplog.text
#     print(caplog.text)


# @pytest.mark.asyncio
# async def test_fetch_matrix_http_error(mock_aiohttp, caplog):
#     url = "http://examplecom/matrix"
#     mock_aiohttp.get(url)

#     async with aiohttp.ClientSession() as session:
#         with pytest.raises(aiohttp.ClientConnectionError):
#             await fetch_matrix(session, url)

#     assert "Ошибка HTTP 404" in caplog.text


# @pytest.mark.asyncio
# async def test_fetch_matrix_http_error(mock_aiohttp, caplog):
#     url: str = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix"
#     mock_aiohttp.get(url, status=404, body="Not Found")

#     async with aiohttp.ClientSession() as session:
#         with pytest.raises(aiohttp.ClientResponseError):
#             await fetch_matrix(session, url)

#     assert "Ошибка HTTP 404" in caplog.text


# @pytest.mark.asyncio
# async def test_fetch_matrix_connection_error(mock_aiohttp, caplog):
#     url = "http://example.com/matrix"
#     mock_aiohttp.get(url, exception=aiohttp.ClientConnectorError(None, Exception("Connection failed")))

#     async with aiohttp.ClientSession() as session:
#         with pytest.raises(aiohttp.ClientConnectorError):
#             await fetch_matrix(session, url)

#     assert "Ошибка соединения" in caplog.text
