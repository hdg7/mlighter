from src.mlighter_utils.conversion import to_float, to_fraction, to_positive, to_positive_or_none, to_greater_than, \
    to_greater_than_or_none, to_positive_integer_or_fraction, to_reserved_or_else, NotReserved, select_from, to_bool, \
    select_function


class TestConversion:
    def test_select_from(self):
        assert select_from(0, [1, 2, 3]) == 1
        assert select_from(1, [1, 2, 3]) == 2
        assert select_from(2, [1, 2, 3]) == 3
        assert select_from(3, [1, 2, 3]) == 1

    def test_to_bool(self):
        assert to_bool(0) is False
        assert to_bool(1) is True
        assert to_bool(2) is False
        assert to_bool(-1) is True

    def test_to_float(self):
        assert to_float(0) == 0.0
        assert to_float(9932) == 4.907e-320
        assert to_float(-1) == 0.0
        assert to_float(-665 * 10 ** 15) == -1.3505803869538944e+264
        assert to_float(4696837150979653632) == 1000000.5

    def test_to_fraction(self):
        assert to_fraction(0) == 0.0
        assert to_fraction(9932) == 4.907e-320
        assert to_fraction(-1) == 0.0
        assert to_fraction(-665 * 10 ** 15) == 0.0
        assert to_fraction(4696837150979653632) == 0.5

    def test_to_positive(self):
        assert to_positive(0) == 0
        assert to_positive(9932) == 9932
        assert to_positive(-1) == 1
        assert to_positive(-665 * 10 ** 15) == 665 * 10 ** 15
        assert to_positive(0.5) == 0.5
        assert to_positive(-0.5) == 0.5

    def test_to_positive_or_none(self):
        assert to_positive_or_none(0) is None
        assert to_positive_or_none(9932) == 9932
        assert to_positive_or_none(-1) is None
        assert to_positive_or_none(-665 * 10 ** 15) is None
        assert to_positive_or_none(0.5) == 0.5
        assert to_positive_or_none(-0.5) is None

    def test_to_greater_than(self):
        assert to_greater_than(0, 0) == 0
        assert to_greater_than(0, 9932) == 9932
        assert to_greater_than(100, -1) == 99
        assert to_greater_than(3, -665 * 10 ** 15) == (-665 * 10 ** 15) + 3
        assert to_greater_than(435, -40) == 395

    def test_to_greater_than_or_none(self):
        assert to_greater_than_or_none(0, 0) is None
        assert to_greater_than_or_none(0, 9932) is None
        assert to_greater_than_or_none(100, -1) == 99
        assert to_greater_than_or_none(3, -665 * 10 ** 15) == (-665 * 10 ** 15) + 3
        assert to_greater_than_or_none(-666 * 10 ** 15, -665 * 10 ** 15) is None

    def test_to_positive_integer_or_fraction(self):
        assert to_positive_integer_or_fraction(0) == 0
        assert to_positive_integer_or_fraction(9932) == 9932
        assert to_positive_integer_or_fraction(-1) == 5e-324
        assert to_positive_integer_or_fraction(-665 * 10 ** 15) == 3.2941511358867378e-264
        assert to_positive_integer_or_fraction(4696837150979653632) == 4696837150979653632
        assert to_positive_integer_or_fraction(-4696837150979653632) == 0.5

    def test_to_reserved_or_else_dict(self):
        reserved_values = {0: 'zero', -1: 'alpha', -2: 'beta'}

        assert to_reserved_or_else(0, reserved_values, to_positive) == 'zero'
        assert to_reserved_or_else(1, reserved_values, to_positive) == 1
        assert to_reserved_or_else(-1, reserved_values, to_positive) == 'alpha'
        assert to_reserved_or_else(-2, reserved_values, to_positive) == 'beta'
        assert to_reserved_or_else(-3, reserved_values, to_positive) == 3

    def test_to_reserved_or_else_function(self):
        def reserved_values(x):
            if x == 0:
                return 'zero'
            elif x == -1:
                return 'alpha'
            elif x == -2:
                return 'beta'
            else:
                return NotReserved

        assert to_reserved_or_else(0, reserved_values, to_positive) == 'zero'
        assert to_reserved_or_else(-1, reserved_values, to_positive) == 'alpha'
        assert to_reserved_or_else(-2, reserved_values, to_positive) == 'beta'
        assert to_reserved_or_else(-3, reserved_values, to_positive) == 3

    def test_to_reserved_or_else_shift(self):
        reserved_values = {0: 'zero', 1: 'alpha', 2: 'beta'}

        def shift(x):
            """Shifts the value by 3 down, ensuring values 3 upwards are still possible"""
            return x - 3

        assert to_reserved_or_else(0, reserved_values, to_positive, shift) == 'zero'
        assert to_reserved_or_else(3, reserved_values, to_positive, shift) == 0

    def test_select_function(self):
        assert select_function(0, lambda x: x % 2, lambda x: x + 1, lambda x: x + 2) == 1
        assert select_function(1, lambda x: x % 2, lambda x: x + 1, lambda x: x + 2) == 3
        assert select_function(2, lambda x: x % 2, lambda x: x + 1, lambda x: x + 2) == 3
        assert select_function(2, lambda x: x % 2 == 0, lambda x: x + 1, lambda x: x + 2) == 4
        assert select_function(2, lambda x: x % 2 != 0, lambda x: x + 1, lambda x: x + 2) == 3
