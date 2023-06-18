from gpu_usage_plotter.gpu_usage_extraction import get_gpu_usage


def test_get_gpu_usage() -> None:
    data_df = get_gpu_usage()

    assert data_df is not None
    assert len(data_df) > 0
    assert len(data_df.columns) == 4
