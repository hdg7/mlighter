import sys
import os
from typing import List

import numpy as np


def load_args_or_default(default_args: List[str]) -> List[str]:
    """Loads args from sys.argv or uses default_args"""
    args = sys.argv
    if len(args) < 2:
        args.append(default_args[0])
    return args


def exit_fuzz() -> None:
    """Exits the program using os._exit(0)"""
    os._exit(0)


def save_input(byte_arr: np.ndarray | List[any], file_name: str) -> None:
    """Saves a binary array (or list which will be converted using a np.int64 encoding) to a file,
    with the extension .npy, then exits"""
    if isinstance(byte_arr, list):
        byte_arr = np.array(byte_arr, dtype=np.int64)
    byte_arr.tofile(file_name + '.npy')
    exit()


def load_input(file_name: str) -> np.ndarray:
    """Loads a binary array from a file, using the data type np.int64"""
    return np.fromfile(file_name, dtype=np.int64)
