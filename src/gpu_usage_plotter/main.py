import time
from typing import TypedDict

import GPUtil
import pandas as pd
import plotly.express as px


class GPUData(TypedDict):
    name: str
    load: float
    memoryUtil: float


class GPUUsagePlotter:
    def __init__(self):
        self.df = pd.DataFrame(columns=["name", "load", "memoryUtil"])

    def update(self, gpu_data: GPUData) -> None:
        self.df = pd.concat([self.df, gpu_data], ignore_index=True)

    def plot(self) -> None:
        fig = px.line(self.df, x=self.df.index, y=["load", "memoryUtil"], color="name")
        return fig


def get_gpu_usage() -> pd.DataFrame:
    data = []
    for gpu in GPUtil.getGPUs():
        gpu_data = GPUData(name=gpu.name, load=gpu.load * 100, memoryUtil=gpu.memoryUtil * 100)
        data.append(gpu_data)

    df = pd.DataFrame(data)
    return df


def main() -> None:
    """
    The core function of this awesome project.
    """

    start_time = time.time()
    idx = 0
    plotter = GPUUsagePlotter()
    while True:
        plotter.update(get_gpu_usage())
        fig = plotter.plot()
        fig.write_html(f"gpu_usage.html")

        print(f"Elapsed time: {time.time() - start_time:.2f} sec")

        time.sleep(1)
        idx += 1


if __name__ == "__main__":
    main()
