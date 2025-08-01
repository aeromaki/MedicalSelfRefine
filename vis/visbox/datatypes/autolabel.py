from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


class AutoLabelFormat(TypedDict):
    id: int
    question: str
    options: str
    response: str
    prediction: str
    label: str

class LabelResult(TypedDict):
    id: int
    data: AutoLabelFormat
    explanation: str
    category: str | None

class Category:
    cat: int | None
    subcat: set[str] | None

    def __init__(self, repr: str | None) -> None:
        try:
            if type(repr) != str:
                raise

            cat, subcat = repr.split(" - ")
            self.cat = int(cat)
            self.subcat = set()

            for s in subcat.split(','):
                ss = s.lower().strip()
                if ss in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    self.subcat.add(ss)
                else:
                    raise

            if len(self.subcat) == 0:
                raise

        except:
            self.cat = None
            self.subcat = None

    def __repr__(self) -> str:
        return f"Category({self.cat} - {", ".join(self.subcat)})"\
                if self.cat is not None and self.subcat is not None\
                else "Category(error)"

    __str__ = __repr__

    def to_ndarray_mat(self) -> npt.NDArray[np.int64]:
        v = np.zeros((4, 7), dtype=int)
        if self.cat is not None and self.subcat is not None:
            for i in self.subcat:
                v[self.cat - 1][ord(i) - 97] = 1
        return v

    def to_ndarray_cat(self) -> npt.NDArray[np.int64]:
        c = np.zeros(4, dtype=int)
        if self.cat is not None:
            c[self.cat - 1] = 1
        return c


@dataclass
class MatCatTuple:
    mat: npt.NDArray[np.floating]
    cat: npt.NDArray[np.floating]

    def __add__(self, x: MatCatTuple) -> MatCatTuple:
        return MatCatTuple(
                self.mat + x.mat,
                self.cat + x.cat
                )

    def __truediv__(self, x: float) -> MatCatTuple:
        return MatCatTuple(
                self.mat / x,
                self.cat / x
                )
    
