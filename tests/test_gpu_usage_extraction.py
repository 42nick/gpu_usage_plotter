"""This test is written with the help of ChatGPT."""
from datetime import datetime
from unittest.mock import Mock

import GPUtil
import pandas as pd
import pytest

from gpu_usage_plotter.gpu_usage_extraction import get_gpu_usage


class MockGPU:
    def __init__(self, name: str, load: float, memoryUtil: float): # pylint: disable=invalid-name
        self.name = name
        self.load = load
        self.memoryUtil = memoryUtil


@pytest.fixture
def mock_get_gpus(monkeypatch):
    """
    Fixture to mock the GPUtil.getGPUs function.

    Args:
        monkeypatch: pytest monkeypatch fixture.

    Returns:
        list: List of mocked GPU objects.
    """
    mocked_gpu_data = [
        MockGPU(name='GPU 1', load=0.5, memoryUtil=0.3),
        MockGPU(name='GPU 2', load=0.8, memoryUtil=0.6),
    ]
    mock_get_gpus = Mock(return_value=mocked_gpu_data)
    monkeypatch.setattr(GPUtil, 'getGPUs', mock_get_gpus)
    return mocked_gpu_data


def test_get_gpu_usage(mock_get_gpus, monkeypatch):
    """
    Test case for the get_gpu_usage function.

    Args:
        mock_get_gpus: Mocked GPU data.
        monkeypatch: pytest monkeypatch fixture.
    """
    expected_columns = ['name', 'load', 'memoryUtil', 'timestamp']
    expected_data = [
        ['GPU 1', 50.0, 30.0, pd.Timestamp('2023-06-24 12:34:56')],
        ['GPU 2', 80.0, 60.0, pd.Timestamp('2023-06-24 12:34:56')],
    ]
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    # Monkeypatching datetime.now() to return a fixed timestamp
    monkeypatch.setattr("gpu_usage_plotter.gpu_usage_extraction.datetime", Mock(now=Mock(return_value=datetime(2023, 6, 24, 12, 34, 56))))

    result_df = get_gpu_usage()

    assert isinstance(result_df, pd.DataFrame)
    assert result_df.equals(expected_df)


def test_get_gpu_usage_no_gpus(monkeypatch):
    """
    Test case for the get_gpu_usage function when no GPUs are available.

    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    monkeypatch.setattr(GPUtil, 'getGPUs', Mock(return_value=[]))

    result_df = get_gpu_usage()

    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 0
