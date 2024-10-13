import os
import threading
import time

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

from gpu_usage_plotter.gpu_usage_extraction import GPUUsageLogger

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


# Initialize the GPU usage logger
gpu_logger = GPUUsageLogger(log_interval=1, save_interval=60, log_duration=3600 * 10)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div(
        [
            html.H4("GPU Usage Plotter"),
            html.Div(id="live-update-text"),
            html.Button("Download Text", id="btn-download-txt"),
            html.Button("Clear History", id="my-button4"),
            dcc.Checklist(
                id="auto-update-checklist",
                options=[{"label": "Auto Update", "value": "auto"}],
                value=["auto"],  # Default to auto-update enabled
                style={"margin": "10px 0"},
            ),
            dcc.Download(id="download-text"),
            dcc.Graph(id="live-update-gpu-load"),
            dcc.Graph(id="live-update-gpu-memory"),
            dcc.Interval(id="interval-component", interval=1 * 1000, n_intervals=0),  # in milliseconds
            dcc.Store(id="gpu_usage_data_store", data=None, storage_type="local"),
        ]
    )
)


# Multiple components can update every time interval gets fired.
@app.callback(
    [
        Output("live-update-gpu-load", "figure"),
        Output("live-update-gpu-memory", "figure"),
        Output("gpu_usage_data_store", "data"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("auto-update-checklist", "value"),
    ],
)
def update_graph_live(n_intervals, auto_update):
    """Updates the graph with the latest GPU usage data."""

    # Check if auto-update is enabled
    if "auto" not in auto_update:
        # Return the current state without updating
        return dash.no_update, dash.no_update, dash.no_update

    data_df = gpu_logger.gpu_usage_data["df"]

    # Create figures
    fig = px.line(data_df, x="timestamp", y=["load"], color="name")
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="GPU-Util in %")

    fig2 = px.line(data_df, x="timestamp", y=["memoryUtil"], color="name")
    fig2.update_layout(xaxis_title="Timestamp", yaxis_title="Memory Usage in %")

    return fig, fig2, gpu_logger.gpu_usage_data["df"].to_dict()


@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    State("gpu_usage_data_store", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, gpu_usage_data_store):
    return dcc.send_data_frame(pd.DataFrame.from_dict(gpu_usage_data_store["df"]).to_csv, "mydf.csv")


@app.callback(Output("gpu_usage_data_store", "clear_data"), [Input("my-button4", "n_clicks")])
def clear_click(n_click_clear):
    if n_click_clear is not None and n_click_clear > 0:
        gpu_logger.gpu_usage_data = {"df": pd.DataFrame().to_dict()}
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True)
