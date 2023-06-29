from flask import Flask

import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px

#app = Flask(__name__)
app = dash.Dash(__name__)   #initialising dash app


#@app.route("/")
#def hello():
#    return "Hello World from simpleApp\n"

#if __name__ == "__main__":
#    # Only for debugging while developing
#    app.run(host='0.0.0.0', debug=True, port=80)


# 
# import dash
# from dash import html
# from dash import dcc
# import plotly.graph_objects as go
# import plotly.express as px
# 
# app = dash.Dash()   #initialising dash app
# df = px.data.stocks() #reading stock price dataset 
# 
# @app.route("/")
# def hello():
#     return "Hello World from simpleApp\n"
# 
# # 
# # def stock_prices():
# #     fig = go.Figure([go.Scatter(x = df['date'], y = df['GOOG'],
# #                      line = dict(color = 'firebrick', width = 4), name = 'Google')
# #                      ])
# #     fig.update_layout(title = 'Prices over time',
# #                       xaxis_title = 'Dates',
# #                       yaxis_title = 'Prices'
# #                       )
# #     return fig  
# # 
# #  
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Styling using html components',
			style = {'textAlign':'center',
            'marginTop':40,'marginBottom':40}),
        dcc.Graph(id = 'line_plot', figure = stock_prices())
    ])
  

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True, port=80)
