import struct
import math

import numpy as np


# TODO: bool, conditionally choose between functions to apply


def select_from(value, options):
    """Selects a value from a list of options"""
    return options[value % len(options)]


def to_bool(value):
    """Converts an int or np.int64 to a bool"""
    return bool(value % 2)


def to_float(value):
    """Converts an int or np.int64 to a float value, if nan or inf, returns 0.0"""
    packed = struct.pack('>q', value)
    unpacked = struct.unpack('>d', packed)[0]

    if math.isnan(unpacked) or math.isinf(unpacked):
        return 0.0
    else:
        return unpacked


def to_fraction(value):
    """Converts an int or np.int64 to a float between 0 and 1"""
    # return abs(float(value) / MAX_INT)
    """
    Using modf as it may scale better than the above.
    Currently untested.
    """
    return math.modf(to_float(value))[0]


def to_positive(value):
    """Converts an int, np.int64, or float to a positive int or float"""
    return abs(value)


def to_positive_or_none(value):
    """Converts an int, np.int64, or float to a positive int or float"""
    if value <= 0:
        return None
    else:
        return value


def to_greater_than(value, min_value):
    """Converts an int or np.int64 to a positive int greater than min_value"""
    return min_value + abs(value)


def to_greater_than_or_none(value, min_value):
    """Converts an int or np.int64 to a positive int greater than min_value"""
    if value <= 0:
        return None
    else:
        return min_value + abs(value)


def to_positive_integer_or_fraction(value):
    """Converts an int or np.int64 to a positive int or fraction"""
    if value <= 0:
        return to_fraction(abs(value))
    else:
        return value


class NotReserved:
    """A not reserved type"""
    pass


def to_reserved_or_else(value, reserved, else_function, shift_function=lambda x: x):
    """
    Takes a value and returns a reserved value or the else_function

    Args: :param value: (int | np.int64) The value to check :param reserved: (dict[int | np.int64, any] | callable[[
    int | np.int64], any]): A dictionary of reserved values or a function which takes a value and returns its
    replacement :param else_function: (callable[[int | np.int64], any]): A function which takes a value and returns
    its replacement :param shift_function: (callable[[int | np.int64], int | np.int64] | None): A function which
    takes a value and returns its replacement, used to shift the value if it is not reserved
    """
    if type(reserved) is dict:
        if value in reserved:
            return reserved[value]
        else:
            if shift_function is not None:
                value = shift_function(value)

            return else_function(value)
    else:
        reserved_value = reserved(value)
        if reserved_value != NotReserved:
            return reserved_value
        else:
            if shift_function is not None:
                value = shift_function(value)

            return else_function(value)


def select_function(value, selection_function, *options):
    """Selects a function to apply to a value based on a selection function which returns an index into the options"""
    selection = selection_function(value)

    if type(selection) is bool:
        selection = int(selection)

    return options[selection % len(options)](value)
