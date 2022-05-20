# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:37:49 2022
@Software: xxx
@author: lovelycorn
"""
import os;
import dash
from dash import dcc
from dash import html
import pandas as pd

path = os.getcwd() + '//report//'
name = '20220519165751.csv'
data = pd.read_csv(path + name)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="数据展示测试页",),
        html.P(
            children="白司伦"
            " 我是"
            " 你爹",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["日期"],
                        "y": data["收盘价"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "闻泰科技价格走势图"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["日期"],
                        "y": data["收益总额"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "闻泰科技收益走势图"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=7966)
    #app.run_server('0.0.0.0', '7965', 'true')
    