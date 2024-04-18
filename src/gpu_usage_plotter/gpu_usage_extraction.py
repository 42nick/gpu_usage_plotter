"""Module for extracting GPU usage data."""

from datetime import datetime
from typing import TypedDict

import GPUtil
import numpy as np
import pandas as pd


class GPUData(TypedDict):
    """Container for GPU data."""

    name: str
    load: float
    memoryUtil: float
    timestamp: datetime


def get_gpu_usage() -> pd.DataFrame:
    data = []
    for gpu in GPUtil.getGPUs():
        gpu_data = GPUData(
            name=gpu.name, load=gpu.load * 100, memoryUtil=gpu.memoryUtil * 100, timestamp=datetime.now()
        )

        # check of load is nan and then replace it with 0
        if np.isnan(gpu_data["load"]):
            gpu_data["load"] = 0

        data.append(gpu_data)

    return pd.DataFrame(data)
