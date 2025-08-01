from typing import Callable
import matplotlib.pyplot as plt
from matplotlib.colors import CenteredNorm, Normalize
import numpy as np
import numpy.typing as npt


CAT_LABELS = ['1', '2', '3', '4']
MAT_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']


def heatmap(
        data: npt.NDArray,
        cmap: str | None = None,
        norm: Normalize | None = None,
        title: str | None = None,
        colorbar: bool = True
        ) -> None:
    plt.imshow(
            data,
            interpolation="none",
            norm=norm,
            cmap=cmap
            )
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            plt.text(
                    j, i, data[i, j].round(3),
                    ha="center",
                    va="center")

    if colorbar:
        plt.colorbar()

    plt.xticks(
            ticks=range(len(MAT_LABELS)),
            labels=MAT_LABELS)
    plt.yticks(
            ticks=range(len(CAT_LABELS)),
            labels=CAT_LABELS
            )

    if title is not None:
        plt.title(title)


def heatmap_log(
        data: npt.NDArray,
        title: str | None = None,
        colorbar: bool = True
        ) -> None:
    heatmap(
            np.log(data + 1e-06),
            cmap="plasma",
            title=title,
            colorbar=colorbar
            )


def heatmap_iteration(
        data_iter: npt.NDArray[np.floating],
        f_subplot: Callable[[int], None],
        colorbar: bool = True,
        clim_min: float = -14,
        clim_max: float = 0
        ) -> None:
    n = data_iter.shape[0]
    for i in range(n):
        f_subplot(i+1)
        heatmap_log(
                data_iter[i],
                title='initial response'\
                        if i == 0 else f'refinement iter {i}',
                colorbar=colorbar
                )
    plt.clim(clim_min, clim_max)
    plt.tight_layout()
        

def heatmap_norm(
        data: npt.NDArray,
        title: str| None = None,
        colorbar: bool = True
        ) -> None:
    heatmap(
            data,
            cmap="coolwarm",
            norm=CenteredNorm(),
            title=title,
            colorbar=colorbar
            )


def heatmap_iteration_diff(
        data_iter: npt.NDArray[np.floating],
        f_subplot: Callable[[int], None],
        colorbar: bool = True,
        clim: float = 0.08
        ) -> None:
    n = data_iter.shape[0]
    for i in range(n-1):
        f_subplot(i+1)
        heatmap_norm(
                data_iter[i+1] - data_iter[i],
                title='initial response → refinement iter 1'\
                        if i == 0\
                        else f'refinement iter {i} → refinement iter {i+1}',
                colorbar=colorbar
                )
    plt.clim(-clim, clim)
    plt.tight_layout()


def plot_cat(cat: npt.NDArray[np.floating]) -> None:
    plt.bar(CAT_LABELS, cat)

def plot_mat(mat: npt.NDArray[np.floating]) -> None:
    plt.bar(MAT_LABELS, mat.sum(0))
