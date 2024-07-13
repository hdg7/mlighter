import os
import sys

import numpy as np

PATH = os.path.dirname(os.path.abspath(__file__))

PATH_TO_DATASETS = PATH + "/data/"

MAX_INT = np.iinfo(np.int64).max
MIN_FLOAT = sys.float_info.min


FIXED_RANDOM_VALUE = 0
