import aiohttp
import pytest

from get_matrix import SOURCE_URL, get_matrix, TRAVERSAL


# Пример корректного тела матрицы из оригинального источника
MOCK_MATRIX_TEXT: str = """| 10 | 20 | 30 | 40|
--------------------
| 50 | 60 | 70 | 80 | 
--------------------
| 90 | 100 | 110 |120|
--------------------
| 130 | 140 | 150 | 160 |"""


@pytest.mark.asyncio
async def test_get_matrix_success(mock_aiohttp):
    """Тест успешного выполнения get_matrix с корректными данными."""
    # Мокаем HTTP-запрос к источнику данных
    mock_aiohttp.get(SOURCE_URL, status=200, body=MOCK_MATRIX_TEXT)
    
    # Выполняем тестируемую функцию
    result = await get_matrix(SOURCE_URL)
    
    # Проверяем, что результат соответствует ожидаемому обходу против часовой стрелки
    assert result == TRAVERSAL


@pytest.mark.asyncio
async def test_get_matrix_http_error(mock_aiohttp):
    """Тест обработки HTTP ошибок при загрузке данных."""
    # Мокаем HTTP-запрос с ошибкой 500
    mock_aiohttp.get(SOURCE_URL, status=500)
    
    # Проверяем, что функция выбрасывает исключение при HTTP ошибке
    with pytest.raises(Exception):
        await get_matrix(SOURCE_URL)


@pytest.mark.asyncio
async def test_get_matrix_connection_error(mock_aiohttp):
    """Тест обработки ошибок соединения."""
    # Мокаем HTTP-запрос с ошибкой соединения
    mock_aiohttp.get(SOURCE_URL, exception=aiohttp.ClientConnectionError())
    
    # Проверяем, что функция выбрасывает исключение при ошибке соединения
    with pytest.raises(Exception):
        await get_matrix(SOURCE_URL)


@pytest.mark.asyncio
async def test_get_matrix_empty_response(mock_aiohttp):
    """Тест обработки пустого ответа от сервера."""
    # Мокаем HTTP-запрос с пустым телом
    mock_aiohttp.get(SOURCE_URL, status=200, body="")
    
    # Проверяем, что функция выбрасывает исключение при пустом ответе
    with pytest.raises(ValueError, match="Пустой ответ от сервера"):
        await get_matrix(SOURCE_URL)


@pytest.mark.asyncio
async def test_get_matrix_invalid_data(mock_aiohttp):
    """Тест обработки некорректных данных в ответе."""
    # Мокаем HTTP-запрос с некорректными данными
    mock_aiohttp.get(SOURCE_URL, status=200, body="invalid data without separators")
    
    # Проверяем, что функция выбрасывает исключение при некорректных данных
    with pytest.raises(ValueError):
        await get_matrix(SOURCE_URL)


@pytest.mark.asyncio
async def test_get_matrix_timeout_error(mock_aiohttp):
    """Тест обработки таймаута при запросе."""
    # Мокаем HTTP-запрос с таймаутом
    mock_aiohttp.get(SOURCE_URL, exception=aiohttp.ServerTimeoutError())
    
    # Проверяем, что функция выбрасывает исключение при таймауте
    with pytest.raises(Exception):
        await get_matrix(SOURCE_URL)
