import asyncio
import logging
from aiohttp import (
    ClientSession,
    ClientConnectorError,
    ClientResponseError,
    ServerDisconnectedError,
    ClientPayloadError,
    ClientTimeout as AiohttpTimeout,
)


# --- Настройка логирования ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("matrix_app.log", encoding="utf-8"),
        logging.StreamHandler(),  # вывод в консоль
    ],
)

logger = logging.getLogger(__name__)

SOURSE_URL: str = (
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


def spiral_counter_clockwise(matrix: list[list[int]]) -> list[int]:
    if not matrix:
        return []
    if len(matrix) == 1:
        return matrix[0]
    else:
        result: list[int] = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

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

    return result


def make_matrix(data: str) -> list[list[int]]:
    numbers_and_lines: list[str] = [i.strip() for i in data.split("|")]
    lines: list[str] = [line for line in numbers_and_lines if not line.isdigit()]
    numbers: list[int] = [int(num) for num in numbers_and_lines if num.isdigit()]

    size: int = len(lines) - 1

    # создание матрицы
    matrix: list[list[int]] = [numbers[i * size : size + size * i] for i in range(size)]

    return matrix


async def fetch_matrix(session: ClientSession, url: str) -> str:
    logger.info("Загрузка данных с %s", url)

    try:
        async with session.get(url) as response:
            # Явно проверяем статус: 5xx — ошибка сервера, 4xx — клиентская ошибка
            if 400 <= response.status < 600:
                logger.error("Ошибка HTTP %d при запросе к %s", response.status, url)
                raise ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Ошибка HTTP {response.status}: сервер вернул ошибку",
                )
            return await response.text()

    except asyncio.TimeoutError:
        logger.error("Таймаут при запросе к %s", url)
        raise TimeoutError(f"Превышен таймаут при запросе к {url}")

    except ClientConnectorError as e:
        logger.error("Не удалось подключиться к %s: %s", url, e)
        raise ConnectionError(
            f"Не удалось подключиться к {url}. Проверьте URL и соединение."
        )

    except ServerDisconnectedError:
        logger.error("Сервер разорвал соединение с %s", url)
        raise ConnectionError(f"Сервер разорвал соединение с {url}")

    except ClientPayloadError as e:
        logger.error("Неполный ответ от сервера %s: %s", url, e)
        raise ConnectionError(
            f"Ошибка при чтении данных от сервера {url}: неполный ответ."
        )

    except Exception as e:
        logger.critical("Неожиданная ошибка при запросе к %s: %s", url, e)
        raise RuntimeError(f"Неожиданная ошибка при запросе к {url}: {e}")


async def get_matrix(url: str) -> list[int]:
    """
    Основная функция: загружает, парсит и обходит матрицу по спирали.
    """

    logger.info("Начало обработки матрицы по URL: %s", url)
    timeout = AiohttpTimeout(total=10)  # 10 секунд на весь запрос
    async with ClientSession(timeout=timeout) as session:
        try:
            response_body: str = await fetch_matrix(session, url)
        except Exception as e:
            logger.error("Ошибка при загрузке данных: %s", e)
            raise  # Проброс исключения наверх

    # matrix и result нужно вынести из блока async with
    # async with — это контекстный менеджер
    # Он нужен только для выполнения асинхронного запроса (await fetch_matrix(...)).

    # make_matrix и spiral_counter_clockwise — синхронные функции
    # Они не работают с сетью, не используют session, им не нужен ClientSession.

    # Сессия (session) должна быть закрыта как можно раньше
    # После async with блока — сессия закрывается (соединения освобождаются).
    # Это хорошая практика: не держать её дольше, чем нужно.

    try:
        matrix: list[list[int]] = make_matrix(response_body)
        logger.info(
            "Матрица успешно распаршена: %d×%d",
            len(matrix),
            len(matrix[0]) if matrix else 0)
        result: list[int] = spiral_counter_clockwise(matrix)
        logger.info("Спиральный обход завершён: %d элементов", len(result))
        return result
    except ValueError as e:
        logger.error("Ошибка парсинга матрицы: %s", e)
        raise ValueError(f"Ошибка при парсинге матрицы: {e}")
    except Exception as e:
        logger.error("Ошибка при обработке матрицы: %s", e)
        raise RuntimeError(f"Ошибка при обработке матрицы: {e}")


if __name__ == "__main__":

    async def main():
        res: list[int] = await get_matrix(SOURSE_URL)
        print(f"Рузультать обохода матрыицы по спирали: {res}")

    asyncio.run(main())


__all__ = ["get_matrix", "spiral_counter_clockwise", "make_matrix"]
# assert asyncio.run(get_matrix(SOURSE_URL)) == TRAVERSAL
