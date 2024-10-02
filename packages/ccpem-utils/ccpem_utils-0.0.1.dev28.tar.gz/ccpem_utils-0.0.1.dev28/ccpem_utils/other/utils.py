import re
from typing import Tuple, List
from warnings import warn
import os


def set_gpu() -> bool:
    try:
        import cupy

        if not cupy.cuda.is_available():
            raise RuntimeError("GPU / CUDA not available, falling back to CPU")
        else:
            os.environ["ENABLE_GPU"] = "True"

    except ImportError:
        warn("Cupy not installed")

    except RuntimeError as e:
        warn(str(e))

    return check_gpu()


def check_gpu():
    try:
        import cupy

        cupy
    except ImportError:
        return False

    if os.environ.get("ENABLE_GPU") == "True":
        return True
    return False


def extract_numeric_from_string(string: str) -> List[str]:
    return re.findall(r"[-+]?(?:\d*\.*\d+)", string)


def find_index_first_number(input_str: str) -> int:
    ind_c = 0
    for c in input_str:
        try:
            int(c)
            return ind_c
        except (ValueError, TypeError):
            pass
        ind_c += 1
    return ind_c


def compare_tuple(tuple1: Tuple, tuple2: Tuple) -> bool:
    for val1, val2 in zip(tuple1, tuple2):
        if type(val2) is float:
            if round(val1, 2) != round(val2, 2):
                return False
        else:
            if val1 != val2:
                return False
    return True
