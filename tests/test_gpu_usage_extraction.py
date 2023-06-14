from gpu_usage_plotter.gpu_usage_extraction import get_gpu_usage


def test_get_gpu_usage() -> None:
    df = get_gpu_usage()

    assert df is not None
    assert len(df) > 0
    assert len(df.columns) == 4
