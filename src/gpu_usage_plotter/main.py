"""Main entry point to start the dash app visualizing the GPU usage or run GPUUsageLogger."""

import argparse
import time

# from gpu_usage_plotter.app import app
from gpu_usage_plotter.appv2 import app, gpu_logger
from gpu_usage_plotter.gpu_usage_extraction import GPUUsageLogger


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the Dash app visualizing the GPU usage or run GPUUsageLogger.")
    parser.add_argument("--port", type=int, default=8050, help="Port to run the Dash app on (default: 8050)")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to run the Dash app on (default: 127.0.0.1)"
    )
    parser.add_argument("--debug", action="store_true", help="Run the Dash app in debug mode")
    parser.add_argument("--no-dash", action="store_true", help="Run without starting the Dash app")
    parser.add_argument(
        "--log_interval", type=float, default=1, help="Interval in seconds to log GPU usage (default: 5)"
    )
    parser.add_argument(
        "--save_interval", type=int, default=60, help="Interval in seconds to store GPU usage logs (default: 60)"
    )
    parser.add_argument(
        "--log_path", type=str, default="gpu_usage.log", help="Output file for GPU usage logs (default: gpu_usage.log)"
    )
    parser.add_argument(
        "-d", "--log_duration", type=int, default=10, help="Duration in seconds to log GPU usage (default: 10)"
    )
    args = parser.parse_args()

    if args.no_dash:
        logger = GPUUsageLogger(
            log_interval=args.log_interval,
            log_path=args.log_path,
            save_interval=args.save_interval,
            log_duration=args.log_duration,
        )
        logger.start_logging()
        time.sleep(args.log_duration)
        print("Stopping logger...")
        logger.stop()
    else:
        gpu_logger.start_logging()
        app.run_server(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
