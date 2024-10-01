import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import random
import datetime
import ffquant.utils.observer_queue as observer_queue

def show_live_timereturn():
    app = dash.Dash(__name__)

    initial_data = {
        'x': [],
        'y': []
    }

    app.layout = html.Div([
        dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        ),
        dcc.Store(id='data-store', data=initial_data)
    ])

    @app.callback(
        Output('live-graph', 'figure'),
        Output('data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('data-store', 'data')]
    )
    def update_graph_live(n, data):
        data['x'].clear()
        data['y'].clear()
        for item in observer_queue.treturn_queue:
            data['x'].append(item["datetime"])
            data['y'].append(item["timereturn"])

        print(f"data: {data}")

        figure = go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='实时数据更新',
                xaxis=dict(title='时间', type='category'),
                yaxis=dict(title='随机数值')
            )
        )
        return figure, data
    app.run_server(debug=True, use_reloader=False)