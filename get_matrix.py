import asyncio
from aiohttp import ClientSession


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


async def fetch_matrix(session, url: str) -> str:
        async with session.get(url) as response:
            response_body: str = await response.text()
            return response_body


async def get_matrix(url: str) -> list[int]:
    async with ClientSession() as session:
        response_body: str = await fetch_matrix(session,url)

    # matrix и result нужно вынести из блока async with
    # async with — это контекстный менеджер
    # Он нужен только для выполнения асинхронного запроса (await fetch_matrix(...)).

    # make_matrix и spiral_counter_clockwise — синхронные функции
    # Они не работают с сетью, не используют session, им не нужен ClientSession.

    # Сессия (session) должна быть закрыта как можно раньше
    # После async with блока — сессия закрывается (соединения освобождаются).
    # Это хорошая практика: не держать её дольше, чем нужно.

    matrix: list[list[int]] = make_matrix(response_body)
    result: list[int] = spiral_counter_clockwise(matrix)

    return result


if __name__ == "__main__":

    async def main():
        res: list[int] = await get_matrix(SOURSE_URL)
        print(res)

    asyncio.run(main())


__all__ = ["get_matrix", "spiral_counter_clockwise", "make_matrix"]
# assert asyncio.run(get_matrix(SOURSE_URL)) == TRAVERSAL
