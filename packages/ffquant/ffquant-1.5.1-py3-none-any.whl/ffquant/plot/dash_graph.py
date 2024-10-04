import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import ffquant.utils.observer_data as observer_data
import ffquant.plot.dash_ports as dash_ports
import getpass
import plotly.express as px
import pandas as pd
import math
import numpy as np
import psutil
import socket
import os

__ALL__ = ['show_perf_live_graph', 'show_perf_bt_graph']

def get_self_ip():
    addrs = psutil.net_if_addrs()
    for _, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET and address.address.startswith('192.168.25.'):
                return address.address

def init_dash_app(port, username):
    app = dash.Dash(
        name=__name__,
        requests_pathname_prefix=f"/user/{username}/proxy/{port}/"
    )
    return app

###########################################################
##################### Live Graph ##########################
###########################################################
def show_perf_live_graph(riskfree_rate=0.01, use_local_dash_url=False, debug=False):
    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(port, username)

    init_metrics_live_graph(app, riskfree_rate, debug)
    portfolio_data = init_portfolio_live_graph(app, debug)
    buysell_data = init_buysell_live_graph(app, debug)
    drawdown_data = init_drawdown_live_graph(app, debug)
    timereturn_data = init_timereturn_live_graph(app, debug)
    position_data = init_position_live_graph(app, debug)

    app.layout = html.Div([
        dash_table.DataTable(
            id='metrics-table',
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Metrics'}, 'width': '50%'},
                {'if': {'column_id': 'Result'}, 'width': '50%'}
            ],
        ),
        dcc.Graph(id='portfolio-graph'),
        dcc.Graph(id='buysell-graph'),
        dcc.Graph(id='drawdown-graph'),
        dcc.Graph(id='timereturn-graph'),
        dcc.Graph(id='position-graph'),
        dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        ),
        dcc.Store(id='portfolio-data-store', data=portfolio_data),
        dcc.Store(id='buysell-data-store', data=buysell_data),
        dcc.Store(id='drawdown-data-store', data=drawdown_data),
        dcc.Store(id='timereturn-data-store', data=timereturn_data),
        dcc.Store(id='position-data-store', data=position_data),
    ])

    server_url = f"https://{os.environ.get('FINTECHFF_JUPYTERHUB_SERVER_URL', 'strategy.sdqtrade.com')}/user/{username}/proxy/{port}"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}/user/{username}/proxy/{port}"

    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True)

######################## Live Overall Metrics #################
def init_metrics_live_graph(app, riskfree_rate = 0.01, debug=False):
    @app.callback(
        Output('metrics-table', 'data'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_metrics_table(n_intervals):
        length = observer_data.portfolio.__len__()
        days_in_year = 252
        minutes_in_day = 6.5 * 60
        total_return = observer_data.portfolio[-1]['portfolio'] / observer_data.portfolio[0]['portfolio'] - 1
        annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
        std_per_minute = np.std([item['timereturn'] for item in observer_data.treturn])
        std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
        sharpe = "NaN"
        if std_annual != 0:
            sharpe = (annual_return - riskfree_rate) / std_annual

        metrics_data = {
            "Metrics": [
                "Total Return",
                "Annualized Return",
                "Annual Return Volatility",
                "Sharpe Ratio"
            ],
            "Result": [
                f"{total_return:.8%}",
                f"{annual_return:.8%}",
                f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                f"{sharpe:.8f}" if sharpe != "NaN" else sharpe
            ]
        }
        return pd.DataFrame(metrics_data).to_dict('records')

######################## Live Portfolio #######################
def init_portfolio_live_graph(app, debug=False):
    portfolio_data = {
        'x': [],
        'y': []
    }

    @app.callback(
        Output('portfolio-graph', 'figure'),
        Output('portfolio-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('portfolio-data-store', 'data')]
    )
    def update_portfolio_graph(n, data):
        data['x'].clear()
        data['y'].clear()
        for item in observer_data.portfolio:
            data['x'].append(item["datetime"])
            data['y'].append(item["portfolio"])

        if debug:
            print(f"portfolio_data: {data}")

        figure = go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='portfolio',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
        return figure, data
    return portfolio_data

######################## Live BuySell #######################
def init_buysell_live_graph(app, debug=False):
    buysell_data = {
        'datetimes': [],
        'prices': [],
        'buy_datetimes': [],
        'buy_prices': [],
        'sell_datetimes': [],
        'sell_prices': []
    }

    @app.callback(
        Output('buysell-graph', 'figure'),
        Output('buysell-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('buysell-data-store', 'data')]
    )
    def update_buysell_graph(n, data):
        data['datetimes'].clear()
        data['prices'].clear()
        for item in observer_data.kline:
            data['datetimes'].append(item["datetime"])
            data['prices'].append(item["close"])

        figure = go.Figure(
            data=[go.Scatter(
                x=data['datetimes'],
                y=data['prices'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='BuySells',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )

        data['buy_datetimes'].clear()
        data['buy_prices'].clear()
        for item in observer_data.buysell:
            if not math.isnan(item['buy']):
                data['buy_datetimes'].append(item['datetime'])
                data['buy_prices'].append(item['price'])
        if len(data['buy_datetimes']) > 0:
            figure.add_trace(
                go.Scatter(
                    x = data['buy_datetimes'],
                    y = data['buy_prices'],
                    mode = "markers",
                    marker = dict(symbol="triangle-up", color="green", size=10),
                    name = "Buys"
                )
            )

        data['sell_datetimes'].clear()
        data['sell_prices'].clear()
        for item in observer_data.buysell:
            if not math.isnan(item['sell']):
                data['sell_datetimes'].append(item['datetime'])
                data['sell_prices'].append(item['price'])
        if len(data['sell_datetimes']) > 0:
            figure.add_trace(
                go.Scatter(
                    x = data['sell_datetimes'],
                    y = data['sell_prices'],
                    mode = "markers",
                    marker = dict(symbol="triangle-down", color="red", size=10),
                    name = "Sells"
                )
            )

        if debug:
            print(f"buysell_data: {data}")

        return figure, data
    return buysell_data

######################## Live Drawdown #######################
def init_drawdown_live_graph(app, debug=False):
    drawdown_data = {
        'x': [],
        'y': []
    }

    @app.callback(
        Output('drawdown-graph', 'figure'),
        Output('drawdown-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('drawdown-data-store', 'data')]
    )
    def update_drawdown_graph(n, data):
        data['x'].clear()
        data['y'].clear()
        for item in observer_data.drawdown:
            data['x'].append(item["datetime"])
            data['y'].append(item["drawdown"])

        if debug:
            print(f"drawdown_data: {data}")

        figure = go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='drawdown',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
        return figure, data
    return drawdown_data

######################## Live Timereturn #######################
def init_timereturn_live_graph(app, debug=False):
    timereturn_data = {
        'x': [],
        'y': []
    }

    @app.callback(
        Output('timereturn-graph', 'figure'),
        Output('timereturn-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('timereturn-data-store', 'data')]
    )
    def update_timereturn_graph(n, data):
        data['x'].clear()
        data['y'].clear()
        for item in observer_data.treturn:
            data['x'].append(item["datetime"])
            data['y'].append(item["timereturn"])

        if debug:
            print(f"timereturn_data: {data}")

        figure = go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='TimeReturn',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
        return figure, data
    return timereturn_data

######################## Live Position #######################
def init_position_live_graph(app, debug=False):
    position_data = {
        'x': [],
        'y': []
    }

    @app.callback(
        Output('position-graph', 'figure'),
        Output('position-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('position-data-store', 'data')]
    )
    def update_position_graph(n, data):
        data['x'].clear()
        data['y'].clear()
        for item in observer_data.position:
            data['x'].append(item["datetime"])
            data['y'].append(item["position"])

        if debug:
            print(f"position_data: {data}")

        figure = go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='position',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
        return figure, data
    return position_data

###########################################################
################# Backtest Graph ##########################
###########################################################
def show_perf_bt_graph(riskfree_rate=0.01, use_local_dash_url=False):
    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(port, username)

    app.layout = html.Div([
        init_metrics_bt_graph(riskfree_rate),
        init_portfolio_bt_graph(),
        init_buysell_bt_graph(),
        init_drawdown_bt_graph()
    ])

    server_url = f"https://{os.environ.get('FINTECHFF_JUPYTERHUB_SERVER_URL', 'strategy.sdqtrade.com')}/user/{username}/proxy/{port}"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}/user/{username}/proxy/{port}"

    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True
    )

######################## Backtest Overall Metrics #################
def init_metrics_bt_graph(riskfree_rate = 0.01):
    length = observer_data.portfolio.__len__()

    days_in_year = 252
    minutes_in_day = 6.5 * 60
    total_return = observer_data.portfolio[-1]['portfolio'] / observer_data.portfolio[0]['portfolio'] - 1
    annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
    std_per_minute = np.std([item['timereturn'] for item in observer_data.treturn])
    std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
    sharpe = "NaN"
    if std_annual != 0:
        sharpe = (annual_return - riskfree_rate) / std_annual

    metrics_data = {
        "Metrics": [
            "Total Return",
            "Annualized Return",
            "Annual Return Volatility",
            "Sharpe Ratio"
        ],
        "Result": [
            f"{total_return:.8%}",
            f"{annual_return:.8%}",
            f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
            f"{sharpe:.8f}" if sharpe != "NaN" else sharpe
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    return dash_table.DataTable(
            data=metrics_df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Metrics'}, 'width': '50%'},
                {'if': {'column_id': 'Result'}, 'width': '50%'}
            ]
    )

######################## Backtest Portfolio #################
def init_portfolio_bt_graph():
    data = {
        "x": [],
        "y": []
    }
    for item in observer_data.portfolio:
        data['x'].append(item["datetime"])
        data['y'].append(item["portfolio"])
    return dcc.Graph(
        id='portfolio-graph',
        figure=go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='portfolio',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
    )

######################## Backtest Buysell #################
def init_buysell_bt_graph():
    dates = []
    prices = []
    for item in observer_data.buysell:
        dates.append(item['datetime'])
        prices.append(item['price'])

    fig = go.Figure(
        px.line(pd.DataFrame({'Time': dates, 'Price': prices}), title='BuySells', x='Time', y='Price'),
    )

    buy_dates = []
    buy_prices = []
    for item in observer_data.buysell:
        if not math.isnan(item['buy']):
            buy_dates.append(item['datetime'])
            buy_prices.append(item['price'])
    fig.add_trace(
        go.Scatter(
            x = buy_dates,
            y = buy_prices,
            mode = "markers",
            marker = dict(symbol="triangle-up", color="green", size=10),
            name = "Buys"
        )
    )

    sell_dates = []
    sell_prices = []
    for item in observer_data.buysell:
        if not math.isnan(item['sell']):
            sell_dates.append(item['datetime'])
            sell_prices.append(item['price'])
    fig.add_trace(
        go.Scatter(
            x = sell_dates,
            y = sell_prices,
            mode = "markers",
            marker = dict(symbol="triangle-down", color="red", size=10),
            name = "Sells"
        )
    )

    return dcc.Graph(
        id="buysell-graph",
        figure=fig
    )

######################## Backtest Drawdown #################
def init_drawdown_bt_graph():
    data = {
        "x": [],
        "y": []
    }
    for item in observer_data.drawdown:
        data['x'].append(item["datetime"])
        data['y'].append(item["drawdown"])
    return dcc.Graph(
        id='drawdown-graph',
        figure=go.Figure(
            data=[go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            )],
            layout=go.Layout(
                title='drawdown',
                xaxis=dict(title='Time', type='category', showticklabels=False),
                yaxis=dict(title='Value')
            )
        )
    )