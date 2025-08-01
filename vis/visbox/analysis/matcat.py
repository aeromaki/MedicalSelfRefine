from typing import Collection

from visbox.datatypes import *

import numpy as np
import numpy.typing as npt


def get_mat_per_iter(results: list[LabelResult]) -> npt.NDArray[np.int64]:
    """N -> (N, C, S)"""
    return np.stack([
        Category(r['category']).to_ndarray_mat() for r in results
        ])

def get_catmean_per_iter(results: list[LabelResult])\
        -> npt.NDArray[np.floating]:
    """N -> C"""
    return np.stack([
        Category(r['category']).to_ndarray_cat() for r in results
        ]).mean(0)

def get_mat_per_model(results: list[list[LabelResult]])\
        -> npt.NDArray[np.floating]:
    """(I, N) -> (I, C, S)"""
    return np.stack([
        get_mat_per_iter(r).mean(0) for r in results
        ])

def get_catmean_per_model(results: list[list[LabelResult]])\
        -> npt.NDArray[np.floating]:
    """(I, N) -> (I, C)"""
    return np.stack(list(map(get_catmean_per_iter, results)))

def calc_mat_cat(results: Collection[list[list[LabelResult]]])\
        -> MatCatTuple:
    mat = np.mean(list(map(get_mat_per_model, results)), axis=0)
    cat = np.mean(list(map(get_catmean_per_model, results)), axis=0)
    return MatCatTuple(mat, cat)


