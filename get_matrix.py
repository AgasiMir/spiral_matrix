import asyncio
import logging
from functools import wraps

from aiohttp import (
    ClientSession,
    ClientResponseError,
    ClientConnectorError,
    ServerDisconnectedError,
    ClientPayloadError,
    ClientTimeout as AiohttpTimeout,
)

# === Настройка логирования ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('matrix_processor.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# === Константы ===
SOURCE_URL: str = (
    "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
)

TRAVERSAL: list[int] = [
    10,
    50,
    90,
    130,
    140,
    150,
    160,
    120,
    80,
    40,
    30,
    20,
    60,
    100,
    110,
    70,
]

# === Декоратор retry для async-функций ===
def retry(_func=None, *, max_retries: int = 3):
    """
    Декоратор для повторных попыток вызова асинхронной функции.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    logger.info(f"Попытка {attempt + 1}/{max_retries} выполнения {func.__name__}")
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Попытка {attempt + 1} из {max_retries} не удалась: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Все {max_retries} попыток выполнения {func.__name__} завершились ошибкой")
                        raise last_exception
                    logger.info(f"Ждем {attempt + 1} сек. перед повтором...")  
                    await asyncio.sleep(attempt + 1) # Задержка перед повторной попыткой

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)

# === Основные функции ===
def spiral_counter_clockwise(matrix: list[list[int]]) -> list[int]:
    """
    Обходит матрицу по спирали против часовой стрелки.
    """
    try:
        logger.info("Начало обхода матрицы по спирали")
        
        if not matrix or not matrix[0]:
            logger.warning("Пустая матрица для обхода")
            return []

        result: list[int] = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        logger.debug(f"Размер матрицы: {len(matrix)}x{len(matrix[0])}, границы: top={top}, bottom={bottom}, left={left}, right={right}")

        while top <= bottom and left <= right:
            # Левая граница: сверху вниз
            for i in range(top, bottom + 1):
                result.append(matrix[i][left])

            # Нижняя граница: слева направо (кроме первого элемента)
            if left < right:
                for i in range(left + 1, right + 1):
                    result.append(matrix[bottom][i])

            # Правая граница: снизу вверх (кроме первого элемента)
            if top < bottom and left < right:
                for i in range(bottom - 1, top - 1, -1):
                    result.append(matrix[i][right])

            # Верхняя граница: справа налево (кроме первого и последнего элементов)
            if top < bottom - 1 and left < right:
                for i in range(right - 1, left, -1):
                    result.append(matrix[top][i])

            # Сужаем границы
            top += 1
            bottom -= 1
            left += 1
            right -= 1

        logger.info(f"Успешный обход матрицы. Получено {len(result)} элементов")
        logger.debug(f"Результат обхода: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при обходе матрицы: {e}")
        raise

def make_matrix(data: str) -> list[list[int]]:
    """
    Парсит строку с разделителями '|' и возвращает матрицу.
    """
    try:
        logger.info("Начало парсинга матрицы из строки")
        
        if not data:
            logger.error("Получены пустые данные для парсинга")
            raise ValueError("Данные для парсинга не могут быть пустыми")

        numbers_and_lines: list[str] = [i.strip() for i in data.split("|")]
        lines: list[str] = [line for line in numbers_and_lines if not line.isdigit()]
        numbers: list[int] = [int(num) for num in numbers_and_lines if num.isdigit()]

        if not numbers:
            logger.error("Не найдены числа в данных для парсинга")
            raise ValueError("Не удалось извлечь числа из данных")

        size: int = len(lines) - 1

        if size <= 0:
            logger.error(f"Некорректный размер матрицы: {size}")
            raise ValueError("Некорректный размер матрицы")

        # Проверяем, что количество чисел соответствует квадратной матрице
        if len(numbers) != size * size:
            logger.error(f"Количество чисел ({len(numbers)}) не соответствует размеру матрицы {size}x{size}")
            raise ValueError("Некорректное количество элементов для формирования матрицы")

        # создание матрицы
        matrix: list[list[int]] = [numbers[i * size : size + size * i] for i in range(size)]

        logger.info(f"Успешно создана матрица {size}x{size}")
        logger.debug(f"Матрица: {matrix}")
        return matrix

    except ValueError as e:
        logger.error(f"Ошибка преобразования данных в матрицу: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании матрицы: {e}")
        raise

@retry
async def fetch_matrix(session: ClientSession, url: str) -> str:
    """
    Загружает тело ответа по URL.
    Использует retry при временных ошибках.
    """
    try:
        logger.info(f"Начало загрузки данных из {url}")
        
        async with session.get(url) as response:
            response.raise_for_status()  # Проверяем статус ответа
            text: str = await response.text()
            
            logger.info(f"Успешно загружены данные, размер: {len(text)} символов")
            logger.debug(f"Первые 500 символов ответа: {text[:500]}...")
            return text

    except ClientResponseError as e:
        logger.error(f"Ошибка HTTP {e.status} при запросе к {url}: {e}")
        raise
    except (ClientConnectorError, ServerDisconnectedError) as e:
        logger.error(f"Ошибка соединения с {url}: {e}")
        raise
    except ClientPayloadError as e:
        logger.error(f"Ошибка чтения данных с {url}: {e}")
        raise
    except asyncio.TimeoutError as e:
        logger.error(f"Таймаут при запросе к {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке данных: {e}")
        raise

async def get_matrix(url: str) -> list[int]:
    """
    Основная функция: загружает, парсит и обходит матрицу.
    """
    logger.info(f"Запуск обработки матрицы из {url}")
    async with ClientSession(timeout=AiohttpTimeout(total=3)) as session:
        try:
            response_body = await fetch_matrix(session, url)

            if not response_body:
                logger.error("Получен пустой ответ от сервера")
                raise ValueError("Пустой ответ от сервера")

        except Exception as e:
            logger.error(f"Ошибка в основной функции get_matrix: {e}")
            raise

    matrix: list[list[int]] = make_matrix(response_body)
    result: list[int] = spiral_counter_clockwise(matrix)
    
    logger.info(f"Успешно завершена обработка матрицы. Результат содержит {len(result)} элементов")
    return result

# === Точка входа ===
if __name__ == "__main__":
    async def main():
        try:
            logger.info("Запуск приложения")
            result: list[int] = await get_matrix(SOURCE_URL)
            print("Результат:", result)
            logger.info("Приложение успешно завершило работу")
        except Exception as e:
            logger.critical(f"Критическая ошибка в приложении: {e}")
            print("Произошла ошибка:", e)

    asyncio.run(main())

__all__: list[str] = ["get_matrix", "spiral_counter_clockwise", "make_matrix"]
