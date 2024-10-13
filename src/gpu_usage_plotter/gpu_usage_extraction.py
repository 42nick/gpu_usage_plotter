"""Module for extracting GPU usage data."""

import signal
import sys
import threading
import time
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

        # check if load is nan and then replace it with 0
        if np.isnan(gpu_data["load"]):
            gpu_data["load"] = 0

        data.append(gpu_data)

    return pd.DataFrame(data)


class GPUUsageLogger:
    def __init__(self, log_interval=0.5, save_interval=60, log_path="gpu_usage.log", log_duration=10):
        self.log_interval = log_interval
        self.save_interval = save_interval
        self.save_path = log_path
        self.run_duration = log_duration
        self.gpu_usage_data = {"df": pd.DataFrame()}
        self._stop_event = threading.Event()
        self._log_thread = threading.Thread(target=self._log_gpu_usage)
        self._save_thread = threading.Thread(target=self._save_to_disk)
        self._log_thread.daemon = True
        self._save_thread.daemon = True

    def start_logging(self):
        self._log_thread.start()
        self._save_thread.start()

    def _log_gpu_usage(self):
        """Background thread to log GPU usage data."""
        start_time = time.time()
        while not self._stop_event.is_set():
            if self.run_duration and (time.time() - start_time) >= self.run_duration:
                self._stop_event.set()
                break
            new_data = get_gpu_usage()
            self.gpu_usage_data["df"] = pd.concat(
                [pd.DataFrame(self.gpu_usage_data["df"]), new_data], ignore_index=True
            )
            time.sleep(self.log_interval)

    def _save_to_disk(self):
        """Background thread to save GPU usage data to disk."""
        start_time = time.time()
        while not self._stop_event.is_set():
            time.sleep(0.1)
            if (time.time() - start_time) >= self.save_interval:
                self.gpu_usage_data["df"].to_csv(self.save_path, index=False)
                start_time = time.time()
        self.gpu_usage_data["df"].to_csv(self.save_path, index=False)

    def stop(self):
        """Stop the logging and saving threads."""
        self._stop_event.set()
        if threading.current_thread() != self._log_thread:
            self._log_thread.join()
        if threading.current_thread() != self._save_thread:
            self._save_thread.join()
        self._save_to_disk()


def signal_handler(sig, frame):
    print("Termination signal received. Stopping logger...")
    gpu_logger.stop()
    sys.exit(0)


if __name__ == "__main__":
    gpu_logger = GPUUsageLogger(log_interval=1, save_interval=60, log_path="gpu_usage_data.csv", log_duration=5)

    # Register signal handlers for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        print(gpu_logger.gpu_usage_data)
        time.sleep(1)
