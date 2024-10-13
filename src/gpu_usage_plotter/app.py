"""This module contains a small dash up that plots the GPU usage of the system and updates the plot automatically."""

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

from gpu_usage_plotter.gpu_usage_extraction import get_gpu_usage

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div(
        [
            html.H4("GPU Usage Plotter"),
            html.Div(id="live-update-text"),
            html.Button("Download Text", id="btn-download-txt"),
            html.Button("Clear History", id="my-button4"),
            dcc.Download(id="download-text"),
            dcc.Graph(id="live-update-gpu-load"),
            dcc.Graph(id="live-update-gpu-memory"),
            dcc.Interval(id="interval-component", interval=1 * 1000, n_intervals=0),  # in milliseconds
            dcc.Store(id="gpu_usage_data", data=None, storage_type="local"),
        ]
    )
)


# Multiple components can update every time interval gets fired.
@app.callback(
    [
        Output("live-update-gpu-load", "figure"),
        Output("live-update-gpu-memory", "figure"),
        Output("gpu_usage_data", "data"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("live-update-gpu-load", "relayoutData"),
        Input("live-update-gpu-memory", "relayoutData"),
    ],
    State("gpu_usage_data", "data"),
)
def update_graph_live(_, relayout_data_load, relayout_data_memory, gpu_usage_data):
    """Updates the graph with the latest GPU usage data."""

    print(relayout_data_load)

    if gpu_usage_data is None:
        gpu_usage_data = {}
        gpu_usage_data["df"] = get_gpu_usage().to_dict()

    data_df = pd.DataFrame.from_dict(gpu_usage_data["df"])
    data_df = pd.concat([data_df, get_gpu_usage()], ignore_index=True)

    # Create figures
    fig = px.line(data_df, x="timestamp", y=["load"], color="name")
    fig.update_layout(xaxis_title="Timestamp", yaxis_title="GPU-Util in %")

    fig2 = px.line(data_df, x="timestamp", y=["memoryUtil"], color="name")
    fig2.update_layout(xaxis_title="Timestamp", yaxis_title="Memory Usage in %")

    # Apply previous layout state if available and valid
    xaxis_range = None
    yaxis_range = None

    if relayout_data_load and isinstance(relayout_data_load, dict):
        if "xaxis.range[0]" in relayout_data_load and "xaxis.range[1]" in relayout_data_load:
            xaxis_range = [relayout_data_load["xaxis.range[0]"], relayout_data_load["xaxis.range[1]"]]
        if "yaxis.range[0]" in relayout_data_load and "yaxis.range[1]" in relayout_data_load:
            yaxis_range = [relayout_data_load["yaxis.range[0]"], relayout_data_load["yaxis.range[1]"]]

    if relayout_data_memory and isinstance(relayout_data_memory, dict):
        if "xaxis.range[0]" in relayout_data_memory and "xaxis.range[1]" in relayout_data_memory:
            xaxis_range = [relayout_data_memory["xaxis.range[0]"], relayout_data_memory["xaxis.range[1]"]]
        if "yaxis.range[0]" in relayout_data_memory and "yaxis.range[1]" in relayout_data_memory:
            yaxis_range = [relayout_data_memory["yaxis.range[0]"], relayout_data_memory["yaxis.range[1]"]]

    if xaxis_range:
        fig.update_xaxes(range=xaxis_range)
        fig2.update_xaxes(range=xaxis_range)
    if yaxis_range:
        fig.update_yaxes(range=yaxis_range)
        fig2.update_yaxes(range=yaxis_range)

    gpu_usage_data["df"] = data_df.to_dict()
    return fig, fig2, gpu_usage_data


@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    State("gpu_usage_data", "data"),
    prevent_initial_call=True,
)
def func(_, gpu_usage_data):
    return dcc.send_data_frame(pd.DataFrame.from_dict(gpu_usage_data["df"]).to_csv, "mydf.csv")


@app.callback(Output("gpu_usage_data", "clear_data"), [Input("my-button4", "n_clicks")])
def clear_click(n_click_clear):
    if n_click_clear is not None and n_click_clear > 0:
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True)
