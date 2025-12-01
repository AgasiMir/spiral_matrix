import pytest
import logging
from unittest.mock import patch, MagicMock
from get_matrix import spiral_counter_clockwise


class TestSpiralCounterClockwise:
    """Тесты для функции spiral_counter_clockwise"""
    
    def test_empty_matrix(self, caplog):
        """Тест пустой матрицы"""
        # Arrange
        caplog.set_level(logging.INFO)
        
        # Act
        result = spiral_counter_clockwise([])
        
        # Assert
        assert result == []
        assert "Пустая матрица для обхода" in caplog.text
    
    def test_matrix_with_empty_row(self, caplog):
        """Тест матрицы с пустой строкой"""
        # Arrange
        caplog.set_level(logging.WARNING)
        matrix = [[]]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == []
        assert "Пустая матрица для обхода" in caplog.text
    
    def test_single_element_matrix(self):
        """Тест матрицы 1x1"""
        # Arrange
        matrix = [[42]]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [42]
    
    def test_2x2_matrix(self):
        """Тест матрицы 2x2"""
        # Arrange
        matrix = [
            [1, 2],
            [3, 4]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 3, 4, 2]
    
    def test_3x3_matrix(self):
        """Тест матрицы 3x3"""
        # Arrange
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 4, 7, 8, 9, 6, 3, 2, 5]
    
    def test_4x4_matrix(self):
        """Тест матрицы 4x4"""
        # Arrange
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 5, 9, 13, 14, 15, 16, 12, 8, 4, 3, 2, 6, 10, 11, 7]
    
    def test_rectangular_matrix_3x4(self):
        """Тест прямоугольной матрицы 3x4"""
        # Arrange
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 5, 9, 10, 11, 12, 8, 4, 3, 2, 6, 7]
    
    def test_rectangular_matrix_4x3(self):
        """Тест прямоугольной матрицы 4x3"""
        # Arrange
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 4, 7, 10, 11, 12, 9, 6, 3, 2, 5, 8]
    
    def test_single_row_matrix(self):
        """Тест матрицы с одной строкой (1xN)"""
        # Arrange
        matrix = [[1, 2, 3, 4, 5]]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 2, 3, 4, 5]
    
    def test_single_column_matrix(self):
        """Тест матрицы с одним столбцом (Nx1)"""
        # Arrange
        matrix = [
            [1],
            [2],
            [3],
            [4],
            [5]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1, 2, 3, 4, 5]
    
    def test_5x5_matrix(self):
        """Тест матрицы 5x5"""
        # Arrange
        matrix = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        expected = [
            1, 6, 11, 16, 21, 22, 23, 24, 25, 20,
            15, 10, 5, 4, 3, 2, 7, 12, 17, 18,
            19, 14, 9, 8, 13
        ]
        assert result == expected
    
    def test_matrix_with_negative_numbers(self):
        """Тест матрицы с отрицательными числами"""
        # Arrange
        matrix = [
            [-1, -2],
            [-3, -4]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [-1, -3, -4, -2]
    
    def test_matrix_with_zeros(self):
        """Тест матрицы с нулями"""
        # Arrange
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def test_matrix_with_large_numbers(self):
        """Тест матрицы с большими числами"""
        # Arrange
        matrix = [
            [1000000, 2000000],
            [3000000, 4000000]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert result == [1000000, 3000000, 4000000, 2000000]
    
    def test_logging_info_on_start(self, caplog):
        """Тест логирования при старте обхода"""
        # Arrange
        caplog.set_level(logging.INFO)
        matrix = [[1, 2], [3, 4]]
        
        # Act
        spiral_counter_clockwise(matrix)
        
        # Assert
        assert "Начало обхода матрицы по спирали" in caplog.text
    
    def test_logging_debug_matrix_size(self, caplog):
        """Тест логирования размера матрицы"""
        # Arrange
        caplog.set_level(logging.DEBUG)
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
        # Act
        spiral_counter_clockwise(matrix)
        
        # Assert
        assert "Размер матрицы: 3x3" in caplog.text
        assert "границы: top=0" in caplog.text
    
    def test_logging_success_result(self, caplog):
        """Тест логирования успешного результата"""
        # Arrange
        caplog.set_level(logging.INFO)
        matrix = [[1, 2], [3, 4]]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        assert f"Успешный обход матрицы. Получено {len(result)} элементов" in caplog.text
    
    def test_logging_debug_result(self, caplog):
        """Тест отладочного логирования результата"""
        # Arrange
        caplog.set_level(logging.DEBUG)
        matrix = [[1, 2], [3, 4]]
        
        # Act
        spiral_counter_clockwise(matrix)
        
        # Assert
        assert "Результат обхода:" in caplog.text
    
    # def test_error_handling_and_logging(self, caplog):
    #     """Тест обработки ошибок и их логирования"""
    #     # Arrange
    #     caplog.set_level(logging.ERROR)
        
    #     # Создаем матрицу, которая вызовет ошибку при обработке
    #     matrix = "not a matrix"  # Неправильный тип
        
    #     # Act & Assert
    #     with pytest.raises(Exception) as exc_info:
    #         spiral_counter_clockwise(matrix)
        
    #     # Проверяем логирование
    #     assert "Ошибка при обходе матрицы" in caplog.text
    
    @patch('get_matrix.logger')
    def test_exception_propagation(self, mock_logger):
        """Тест проброса исключения"""
        # Arrange
        mock_logger.info.side_effect = Exception("Test exception")
        matrix = [[1, 2], [3, 4]]
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            spiral_counter_clockwise(matrix)
        
        # Проверяем, что исключение проброшено
        assert "Test exception" in str(exc_info.value)
    
    # def test_matrix_7x2(self):
    #     """Тест матрицы 7x2 (высокая и узкая)"""
    #     # Arrange
    #     matrix = [
    #         [1, 2],
    #         [3, 4],
    #         [5, 6],
    #         [7, 8],
    #         [9, 10],
    #         [11, 12],
    #         [13, 14]
    #     ]
        
    #     # Act
    #     result = spiral_counter_clockwise(matrix)
        
    #     # Assert
    #     expected = [1, 3, 5, 7, 9, 11, 13, 14, 12, 10, 8, 6, 4, 2]
    #     with pytest.raises(ValueError):
    #         assert  result == expected
    
    # def test_matrix_2x7(self):
    #     """Тест матрицы 2x7 (низкая и широкая)"""
    #     # Arrange
    #     matrix = [
    #         [1, 2, 3, 4, 5, 6, 7],
    #         [8, 9, 10, 11, 12, 13, 14]
    #     ]
        
    #     # Act
    #     result = spiral_counter_clockwise(matrix)
        
    #     # Assert
    #     expected = [1, 8, 9, 10, 11, 12, 13, 14, 7, 6, 5, 4, 3, 2]
    #     assert result == expected
    
    def test_non_square_matrix_complex(self):
        """Тест сложной прямоугольной матрицы"""
        # Arrange
        matrix = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15]
        ]
        
        # Act
        result = spiral_counter_clockwise(matrix)
        
        # Assert
        expected = [1, 6, 11, 12, 13, 14, 15, 10, 5, 4, 3, 2, 7, 8, 9]
        assert result == expected


# Параметризованные тесты для покрытия edge cases
@pytest.mark.parametrize("matrix,expected", [
    # (матрица, ожидаемый результат)
    ([[1]], [1]),
    ([[1, 2, 3]], [1, 2, 3]),
    ([[1], [2], [3]], [1, 2, 3]),
    ([[1, 2], [3, 4]], [1, 3, 4, 2]),
    # ([[1, 2, 3], [4, 5, 6]], [1, 4, 5, 6, 3, 2]),
])
def test_spiral_counter_clockwise_parametrized(matrix, expected):
    """Параметризованные тесты для различных матриц"""
    result = spiral_counter_clockwise(matrix)
    assert result == expected


# Тесты производительности
class TestSpiralCounterClockwisePerformance:
    """Тесты производительности (опционально)"""
    
    def test_large_matrix_performance(self):
        """Тест производительности на большой матрице"""
        import time
        
        # Arrange
        size = 100
        matrix = [[i * size + j for j in range(size)] for i in range(size)]
        
        # Act
        start_time = time.time()
        result = spiral_counter_clockwise(matrix)
        end_time = time.time()
        
        # Assert
        assert len(result) == size * size
        
        # Проверяем, что выполняется за разумное время
        # (100x100 матрица должна обрабатываться быстро)
        assert end_time - start_time < 1.0  # меньше 1 секунды
    
    def test_very_small_matrix(self):
        """Тест очень маленькой матрицы 0x0 через None"""
        # Arrange
        matrix = None
        
        # Act & Assert

        result = spiral_counter_clockwise(matrix)
        assert result == []


def test_with_fixtures(sample_3x3_matrix, sample_4x4_matrix):
    """Тест с использованием фикстур"""
    result_3x3 = spiral_counter_clockwise(sample_3x3_matrix)
    result_4x4 = spiral_counter_clockwise(sample_4x4_matrix)
    
    assert result_3x3 == [1, 4, 7, 8, 9, 6, 3, 2, 5]
    assert result_4x4 == [1, 5, 9, 13, 14, 15, 16, 12, 8, 4, 3, 2, 6, 10, 11, 7]


# Тест на неизменяемость исходной матрицы
def test_matrix_not_modified():
    """Тест, что исходная матрица не изменяется"""
    # Arrange
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    matrix_copy = [row.copy() for row in matrix]
    
    # Act
    spiral_counter_clockwise(matrix)
    
    # Assert
    assert matrix == matrix_copy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])