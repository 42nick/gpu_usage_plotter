"""Main entry point to start the dash app visualizing the GPU usage."""

import argparse
from gpu_usage_plotter.app import app


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the Dash app visualizing the GPU usage.")
    parser.add_argument("--port", type=int, default=8050, help="Port to run the Dash app on (default: 8050)")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to run the Dash app on (default: 127.0.0.1)"
    )
    parser.add_argument("--debug", action="store_true", help="Run the Dash app in debug mode")
    args = parser.parse_args()

    app.run_server(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
