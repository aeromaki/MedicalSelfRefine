from typing import Any, ParamSpec, TypeVar, Callable
from functools import wraps
import json
import os

from langchain_community.callbacks import get_openai_callback # type: ignore


LOG_PATH = "logs"
RESULT_PATH = "results"


def log_fmt(x: str) -> str:
    return os.path.join(LOG_PATH, f"sr_medqa_2i_{x}_{x}_{x}.json")

def result_fmt(x: str) -> str:
    return os.path.join(RESULT_PATH, f"label_2i_{x}.json")

def load_json(x: str) -> Any:
    return json.load(open(x))


_P = ParamSpec("_P")
_T = TypeVar("_T")

def track_cost(f: Callable[_P, _T]) -> Callable[_P, tuple[_T, float]]:
    @wraps(f)
    def f_tracking(*args: _P.args, **kwargs: _P.kwargs) -> tuple[_T, float]:
        with get_openai_callback() as cb:
            result = f(*args, **kwargs)
            return (result, cb.total_cost)
    return f_tracking
