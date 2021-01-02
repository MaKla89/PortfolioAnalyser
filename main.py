import database
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px


port = database.Portfolio()
port.update_portfolio()
df = port.portfolio

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(external_stylesheets=external_stylesheets, title="Portfolio Analyser")

allocation = px.pie(df, values="Current Value", names="Name")
holdings_perf = px.bar(df, x="Name", y="Profit / Loss")

app.layout = html.Div(children=[
    html.H1(children="Portfolio Analyser",
            style={"textAlign": "center"}),

    html.Div([
        html.Button(children="Load / Refresh Data", id='refresh', n_clicks=0, style={"margin-top": 20}),
    ], style={"text-align": "center", "margin-bottom": 50}),

    html.Div(className="row", style={"textAlign": "center", "font-size": "2em"}, children=[
        html.Div(className="three columns", children=[
            html.H2(children="Total Value"),
        ]),

        html.Div(className="three columns", children=[
            html.H2(children="Total Investment"),
        ]),

        html.Div(className="three columns", children=[
            html.H2(children="Absolute Profit"),
        ]),

        html.Div(className="three columns", children=[
            html.H2(children="Relative Profit"),
        ]),
    ]),

    html.Div(className="row", style={"textAlign": "center", "font-size": "2em"}, children=[
        html.Div(className="three columns", children=[
            html.P(id="total_value", children=str(port.total_worth) + " €")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_invest", children=str(port.total_investment) + " €")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL", children=str(port.total_profit_loss) + " €")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL_rel", children=str(port.total_profit_loss_rel) + " %")
        ]),
    ]),

    html.Div(children=[
        html.H2(children="Asset Allocation",
                style={"textAlign": "center", "marginTop": 50}),
        dcc.Graph(
            id='allocation',
            figure=allocation,
            style={"font_size": "2em"}
        )
    ]),

    html.Div(children=[
        html.H2(children="Holdings & Performance",
                style={"textAlign": "center"}),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict(orient='records'),
            style_table={'overflowX': 'scroll'},
            style_data={"font-size": "1.5em", "textAlign": "center"},
            style_header={"font-size": "1.6em", "font-weight": "bold", "height": "50px", "textAlign": "center"}
        ),
    ]),

    html.Div(children=[
        html.H2(children="Profits & Losses per Position",
                style={"textAlign": "center"}),
        dcc.Graph(
            id='holdings_performance',
            figure=holdings_perf
        )
    ],style={"marginTop": 50})

], style={"border": "50px white solid"})


@app.callback(Output("table", "data"),
              Output("allocation", "figure"),
              Output("holdings_performance", "figure"),
              Output("total_value", "children"),
              Output("total_invest", "children"),
              Output("total_PL", "children"),
              Output("total_PL_rel", "children"),
              Input("refresh", "n_clicks"))
def update(n_clicks):
    print("Update triggered!")
    port.load_portfolio()
    port.update_portfolio()
    df_temp = port.portfolio
    figure1 = px.pie(df, values="Current Value", names="Name")
    figure2 = px.bar(df, x="Name", y= "Profit / Loss")
    total_worth = str(port.total_worth)+" €"
    total_invest = str(port.total_investment)+" €"
    total_pl = str(port.total_profit_loss)+" €"
    total_pl_rel = str(port.total_profit_loss_rel)+" %"

    return df_temp.to_dict(orient='records'), figure1, figure2, total_worth, total_invest, total_pl, total_pl_rel


app.run_server(debug=False, host="0.0.0.0", port=8085)





