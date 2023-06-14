"""Main entry point to start the dash app visualizing the GPU usage."""
from gpu_usage_plotter.app import app


def main() -> None:
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
