import database
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


port = database.Portfolio()
port.update_portfolio()
df = port.portfolio

app = dash.Dash(title="Portfolio Analyser")

allocation = go.Figure()
holdings_perf = go.Figure()

app.layout = html.Div(children=[
    html.H1(children="Portfolio Analyser",
            style={"textAlign": "center"}),

    html.Div([
        html.Button(children="Load / Refresh Data", id='refresh', n_clicks=0, style={"margin-top": 20}),
    ], style={"text-align": "center", "margin-bottom": 50}),

    html.Div(className="row", style={"textAlign": "center", "font-size": "2em"}, children=[
        html.Div(className="two columns", children=[
            html.H2(children="Total Value"),
        ]),

        html.Div(className="two columns", children=[
            html.H2(children="Total Investment"),
        ]),

        html.Div(className="two columns", children=[
            html.H2(children="Total Realised"),
        ]),

        html.Div(className="six columns", children=[
            html.H2(children="Absolute and Relative Profit incl. Realised Positions"),
        ]),

        # html.Div(className="three columns", children=[
        #     html.H2(children="Rel. Profit incl. Realised Positions"),
        # ]),
    ]),

    html.Div(className="row", style={"textAlign": "center", "font-size": "1.8em"}, children=[
        html.Div(className="two columns", children=[
            html.P(id="total_value", children=str(port.total_worth) + " €")
        ]),

        html.Div(className="two columns", children=[
            html.P(id="total_invest", children=str(port.total_investment) + " €")
        ]),

        html.Div(className="two columns", children=[
            html.P(id="total_realised", children=str(port.total_realized_pl) + " €")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL", children=str(port.total_profit_loss) + " €")
        ]),

        html.Div(className="three columns", children=[
            html.P(id="total_PL_rel", children=str(port.total_profit_loss_rel) + " %")
        ]),
    ]),

    html.Div(children=[

        html.H2(children="Asset Allocation", style={"textAlign": "center", "marginTop": 50}),

        html.Div(children=[
            dcc.Graph(
                id='allocation',
                figure=allocation,
            )
        ]),
    ]),

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

    html.Div(children=[
        html.H2(children="Profits & Losses per Position",
                style={"textAlign": "center"}),
        dcc.Graph(
            id='holdings_performance',
            figure=holdings_perf
        )
    ], style={"marginTop": 50})

], style={"border": "50px white solid"})


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

    allocation = px.sunburst(new_df, values="Current Value", path=["Asset Class", "Name"],
                             color_discrete_sequence=px.colors.qualitative.Dark2)
    allocation.update_traces(textinfo="label+percent entry", insidetextorientation='auto',  textfont_size=24)
    allocation.layout.update({"height": 700}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    holdings_perf = px.bar(new_df, x="Name", y=["Realized P/L", "Profit / Loss"],
                           color_discrete_sequence=px.colors.qualitative.Dark2)
    holdings_perf.update_traces(textfont_size=24)
    holdings_perf.layout.update({"height": 700}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    total_worth = str(port.total_worth)+" €"
    total_invest = str(port.total_investment)+" €"
    total_realised = str(port.total_realized_pl)+" €"
    total_pl = str(port.total_profit_loss)+" €"
    total_pl_rel = str(port.total_profit_loss_rel)+" %"

    return [new_df.to_dict(orient='records'),
            allocation,
            holdings_perf,
            total_worth,
            total_invest,
            total_realised,
            total_pl,
            total_pl_rel]


app.run_server(debug=False, host="0.0.0.0", port=8085)





