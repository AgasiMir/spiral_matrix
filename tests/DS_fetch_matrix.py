import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import aiohttp
from aiohttp import ClientResponseError
import asyncio

# Предполагаем, что fetch_matrix находится в модуле get_matrix
from get_matrix import fetch_matrix


class TestFetchMatrix:
    """Тесты для функции fetch_matrix"""
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_success(self):
        """Тест успешного получения данных"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        expected_text = "test data"
        
        # Правильный мок для асинхронного контекстного менеджера
        mock_response.text = AsyncMock(return_value=expected_text)
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/matrix.txt"
        
        # Act
        result = await fetch_matrix(mock_session, url)
        
        # Assert
        mock_session.get.assert_awaited_once_with(url)
        mock_response.text.assert_awaited_once()
        mock_response.raise_for_status.assert_awaited_once()
        assert result == expected_text
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_http_error(self):
        """Тест ошибки HTTP (например, 404)"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        
        # Симулируем HTTP ошибку
        mock_response.raise_for_status = AsyncMock(side_effect=ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=404,
            message="Not Found"
        ))
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/not-found.txt"
        
        # Act & Assert
        with pytest.raises(ClientResponseError) as exc_info:
            await fetch_matrix(mock_session, url)
        
        assert exc_info.value.status == 404
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_connection_error(self):
        """Тест ошибки соединения"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=aiohttp.ClientConnectorError(
            connection_key=MagicMock(),
            os_error=ConnectionError("Connection refused")
        ))
        
        url = "http://unreachable-server.com/matrix.txt"
        
        # Act & Assert
        with pytest.raises(aiohttp.ClientConnectorError):
            await fetch_matrix(mock_session, url)
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_server_disconnected(self):
        """Тест отключения сервера во время запроса"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=aiohttp.ServerDisconnectedError("Server disconnected"))
        
        url = "http://unstable-server.com/matrix.txt"
        
        # Act & Assert
        with pytest.raises(aiohttp.ServerDisconnectedError):
            await fetch_matrix(mock_session, url)
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_payload_error(self):
        """Тест ошибки чтения payload"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        
        # Симулируем ошибку при чтении текста
        mock_response.text = AsyncMock(side_effect=aiohttp.ClientPayloadError("Payload error"))
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/corrupted.txt"
        
        # Act & Assert
        with pytest.raises(aiohttp.ClientPayloadError):
            await fetch_matrix(mock_session, url)
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_timeout(self):
        """Тест таймаута запроса"""
        # Arrange
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=asyncio.TimeoutError("Request timeout"))
        
        url = "http://slow-server.com/matrix.txt"
        
        # Act & Assert
        with pytest.raises(asyncio.TimeoutError):
            await fetch_matrix(mock_session, url)
    
    @pytest.mark.asyncio
    async def test_fetch_matrix_retry_logic(self):
        """Тест логики повторных попыток через декоратор @retry"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        expected_text = "success after retry"
        
        # Первые две попытки падают, третья успешна
        mock_response.text = AsyncMock(return_value=expected_text)
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        side_effects = [
            aiohttp.ServerDisconnectedError("First fail"),
            aiohttp.ServerDisconnectedError("Second fail"),
            mock_response
        ]
        
        mock_session.get = AsyncMock(side_effect=side_effects)
        
        url = "http://flaky-server.com/matrix.txt"
        
        # Act
        result = await fetch_matrix(mock_session, url)
        
        # Assert
        assert mock_session.get.call_count == 3  # 3 попытки
        assert result == expected_text
    
    @pytest.mark.asyncio
    async def test_fetch_max_retries_exceeded(self):
        """Тест превышения максимального количества попыток"""
        # Arrange
        mock_session = AsyncMock()
        
        # Все попытки падают
        mock_session.get = AsyncMock(side_effect=aiohttp.ServerDisconnectedError("Always fails"))
        
        url = "http://dead-server.com/matrix.txt"
        
        # Act & Assert
        with pytest.raises(aiohttp.ServerDisconnectedError):
            await fetch_matrix(mock_session, url)
        
        # Проверяем, что было 3 попытки (значение по умолчанию в декораторе)
        assert mock_session.get.call_count == 3
    
    @pytest.mark.asyncio
    async def test_fetch_empty_response(self):
        """Тест получения пустого ответа"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        
        mock_response.text = AsyncMock(return_value="")  # Пустой ответ
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/empty.txt"
        
        # Act
        result = await fetch_matrix(mock_session, url)
        
        # Assert
        assert result == ""
    
    @pytest.mark.asyncio
    async def test_fetch_large_response(self):
        """Тест получения большого ответа"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        
        large_data = "x" * 1000000  # 1MB данных
        mock_response.text = AsyncMock(return_value=large_data)
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/large.txt"
        
        # Act
        result = await fetch_matrix(mock_session, url)
        
        # Assert
        assert len(result) == 1000000
        assert result == large_data
    
    @pytest.mark.asyncio
    async def test_fetch_with_specific_status_check(self):
        """Тест проверки статуса ответа"""
        # Arrange
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        
        # Симулируем успешный статус
        mock_response.text = AsyncMock(return_value="OK")
        mock_response.raise_for_status = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session.get = AsyncMock(return_value=mock_response)
        
        url = "http://test.com/matrix.txt"
        
        # Act
        await fetch_matrix(mock_session, url)
        
        # Assert
        mock_response.raise_for_status.assert_awaited_once()


# Упрощенная версия с использованием паттерна
@pytest.mark.asyncio
async def test_fetch_matrix_simplified():
    """Упрощенный тест с использованием asynctest паттерна"""
    # Arrange
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    
    # Настраиваем mock объекты
    mock_response.text = AsyncMock(return_value="test data")
    mock_response.raise_for_status = AsyncMock()
    
    # Важно: для асинхронного контекстного менеджера
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    mock_session.get = AsyncMock(return_value=mock_response)
    
    # Act
    result = await fetch_matrix(mock_session, "http://test.com")
    
    # Assert
    assert result == "test data"


# Альтернативный подход с использованием patch
class TestFetchMatrixWithPatch:
    """Тесты с использованием patch для мока aiohttp"""
    
    @pytest.mark.asyncio
    async def test_fetch_with_patch(self):
        """Тест с patch для ClientSession"""
        with patch('aiohttp.ClientSession') as mock_session_class:
            # Arrange
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            
            mock_response.text = AsyncMock(return_value="patched data")
            mock_response.raise_for_status = AsyncMock()
            mock_response.__aenter__ = AsyncMock(return_value=mock_response)
            mock_response.__aexit__ = AsyncMock(return_value=None)
            
            mock_session.get = AsyncMock(return_value=mock_response)
            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)
            
            from get_matrix import get_matrix
            
            # Act & Assert
            # Здесь нужно мокать всю цепочку, так как get_matrix создает свою сессию
            result = await get_matrix("http://test.com")
            
            # Проверяем, что сессия была создана
            mock_session_class.assert_called_once()


# Вспомогательные фикстуры
@pytest.fixture
def mock_aiohttp_response():
    """Фикстура для создания мок-ответа"""
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value="fixture data")
    mock_response.raise_for_status = AsyncMock()
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    return mock_response


@pytest.fixture
def mock_aiohttp_session(mock_aiohttp_response):
    """Фикстура для создания мок-сессии"""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_aiohttp_response)
    return mock_session


@pytest.mark.asyncio
async def test_fetch_matrix_with_fixture(mock_aiohttp_session, mock_aiohttp_response):
    """Тест с использованием фикстуры"""
    result = await fetch_matrix(mock_aiohttp_session, "http://test.com")
    
    assert result == "fixture data"
    mock_aiohttp_session.get.assert_awaited_once_with("http://test.com")
    mock_aiohttp_response.text.assert_awaited_once()
    mock_aiohttp_response.raise_for_status.assert_awaited_once()


# Тест с реальным HTTP сервером (aiohttp тестовый сервер)
@pytest.mark.asyncio
async def test_fetch_from_real_test_server(aiohttp_server):
    """Тест с реальным тестовым сервером"""
    from aiohttp import web
    
    # Создаем тестовое приложение
    async def handler(request):
        return web.Response(text="10|20|30|40")
    
    app = web.Application()
    app.router.add_get("/matrix.txt", handler)
    
    # Запускаем тестовый сервер
    server = await aiohttp_server(app)
    
    # Используем реальную сессию
    async with aiohttp.ClientSession() as session:
        url = f"http://{server.host}:{server.port}/matrix.txt"
        result = await fetch_matrix(session, url)
        
        assert result == "10|20|30|40"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])