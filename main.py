import database
import dash
import dash_auth
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import os.path
import waitress


port = database.Portfolio()
port.update_portfolio()
df = port.portfolio

app = dash.Dash(title="Portfolio Analyser")

try:
    if os.path.isfile("data/basic_auth.txt"):
        print("INFO: Found auth credentials in 'basic_auth.txt', resuming with basic-auth ENABLED")
        f = open("data/basic_auth.txt", "r")
        auth_cred_pair_raw = f.read().splitlines()
        auth_cred_pair = {auth_cred_pair_raw[0]: auth_cred_pair_raw[1]}
        f.close()
        auth = dash_auth.BasicAuth(app, auth_cred_pair)
    else:
        print("WARNING: Could not find or load 'basic_auth.txt' file, resuming with basic-auth DISABLED!")
except Exception as e:
    print("WARNING: Could not find or load 'basic_auth.txt' file, resuming with basic-auth DISABLED!")
    print(e)


allocation = go.Figure()
holdings_perf = go.Figure()

app.layout = html.Div(children=[
    html.H1(children="Portfolio Analyser",
            style={"textAlign": "center", "font-size": "8rem", "font-weight": "780"}),

    html.Div([
        html.Button(children="Load / Refresh Data", id='refresh', n_clicks=0, style={"margin-top": 20}),
    ], style={"text-align": "center", "margin-bottom": 50}),

    html.Hr(),

    html.Div(className="row", style={"textAlign": "center", "font-size": "2em"}, children=[
        html.Div(className="two columns", children=[
            html.H4(children=["Total", html.Br(), "Value"]),
        ]),

        html.Div(className="two columns", children=[
            html.H4(children="Total Investment"),
        ]),

        html.Div(className="two columns", children=[
            html.H4(children="Total Realised"),
        ]),

        html.Div(className="six columns", children=[
            html.H4(children="Absolute and Relative Profit incl. Realised Positions"),
        ]),
    ]),

    html.Div(className="row", style={"textAlign": "center", "font-size": "1.5em"}, children=[
        html.Div(className="two columns", children=[
            html.P(id="total_value")
        ]),

        html.Div(className="two columns", children=[
            html.P(id="total_invest")
        ]),

        html.Div(className="two columns", children=[
            html.P(id="total_realised")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL_rel")
        ]),
    ]),

    html.Hr(),

    html.Div(children=[

        html.H2(children="Asset Allocation", style={"textAlign": "center", "marginTop": 50}),

        html.Div(children=[
            dcc.Graph(
                id='allocation',
                figure=allocation,
            )
        ]),
    ]),

    html.Hr(),

    html.Div(children=[
        html.H2(children="Holdings & Performance",
                style={"textAlign": "center"}),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict(orient='records'),
            style_table={'overflowX': 'scroll'},
            style_data={"font-size": "1.5em",
                        "backgroundColor": "rgba(0,0,0,0)",
                        "textAlign": "center"},
            style_header={"font-size": "1.6em",
                          "font-weight": "bold",
                          "height": "50px",
                          "backgroundColor": "rgba(0,0,0,0)",
                          "textAlign": "center"},

        ),
    ]),

    html.Hr(),

    html.Div(children=[
        html.H2(children="Profits & Losses per Position",
                style={"textAlign": "center"}),
        dcc.Graph(
            id='holdings_performance',
            figure=holdings_perf
        )
    ], style={"marginTop": 50})

], style={"max-width": "1080px", "margin-inline": "auto"})


@app.callback(Output("table", "data"),
              Output("allocation", "figure"),
              Output("holdings_performance", "figure"),
              Output("total_value", "children"),
              Output("total_invest", "children"),
              Output("total_realised", "children"),
              Output("total_PL", "children"),
              Output("total_PL_rel", "children"),
              Input("refresh", "n_clicks"))
def update(n_clicks):
    print("Update triggered!")
    port.load_portfolio()
    port.update_portfolio()
    new_df = port.portfolio

    allocation = px.sunburst(new_df,
                             values="Current Value",
                             path=["Asset Class", "Name"],
                             color_discrete_sequence=px.colors.qualitative.Dark2)
    allocation.update_traces(textinfo="label+percent entry",
                             insidetextorientation='auto',
                             textfont_size=24,
                             marker=dict(line=dict(color='#FFFFFF', width=2)))
    allocation.layout.update({"height": 700},
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)')

    holdings_perf = px.bar(new_df,
                           x="Name",
                           y=["Realized P/L", "Profit / Loss"],
                           orientation='h',
                           color_discrete_sequence=px.colors.qualitative.Dark2)
    holdings_perf.update_traces(textfont_size=24)
    holdings_perf.layout.update({"height": 700},
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)')

    total_worth = str(round(port.total_worth))+" €"
    total_invest = str(round(port.total_investment))+" €"
    total_realised = str(round(port.total_realized_pl))+" €"
    total_pl = str(round(port.total_profit_loss))+" €"
    total_pl_rel = str(round(port.total_profit_loss_rel, 1))+" %"

    return [new_df.to_dict(orient='records'),
            allocation,
            holdings_perf,
            total_worth,
            total_invest,
            total_realised,
            total_pl,
            total_pl_rel]


if __name__ == "__main__":
    waitress.serve(app.server, host="0.0.0.0", port=8085)




