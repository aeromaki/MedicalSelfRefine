from visbox.datatypes import *
from visbox.autolabel import load_model_logs

import numpy as np
import numpy.typing as npt


def get_log_matrix(result_dict: ResultDict) -> npt.NDArray[np.bool]:
    return np.array([g['result'] for g in result_dict['generations']])


