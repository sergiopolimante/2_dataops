import pytest
from src.calculator import add, subtract, multiply, divide


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -1) == -2

    def test_mixed_signs(self):
        assert add(-1, 3) == 2

    def test_floats(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_zeros(self):
        assert add(0, 0) == 0


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(5, 3) == 2

    def test_result_negative(self):
        assert subtract(3, 5) == -2

    def test_zeros(self):
        assert subtract(0, 0) == 0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_mixed_signs(self):
        assert multiply(-2, 3) == -6


class TestDivide:
    def test_exact_division(self):
        assert divide(10, 2) == 5

    def test_float_result(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_negative_division(self):
        assert divide(-6, 3) == -2
