import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools
import plotly.plotly as py
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from dateutil import parser
import pandas as pd
import sundial


def get_battery_output(date):
    usage_kWhr = 8
    t_start = 18  # 6:00pm, sun goes down
    t_final = 22  # 10:00pm, this means battery stops at 10:00pm, not 10:59
    # date = 343  # Dec 9th
    cap_kWhr = 100  # battery capacity
    cost_mult = 10 * cap_kWhr  # cost scales with capacity, adjust to make relavent if needed

    # Compute battery degradation cost per hour.
    battery_cph = sundial.battery_model.bat_price_per_hour(usage_kWhr,
                                                           t_start,
                                                           t_final,
                                                           date,
                                                           cap_kWhr,
                                                           cost_mult)

    return battery_cph


def get_price_output(date):
    epm = sundial.price_model.EnergyPriceModel()
    price_cph = epm.test_model(date, "SVM_rbf")
    return price_cph


def get_pv_output():
    pv_output_cph = sundial.pv_model.pv_output_cph()  # (month,day)
    return pv_output_cph

def get_demand_output():
    # demand_cph = sundial.demand_model.get_demand_cph()
    demand_cph = pd.read_csv("sundial/data/demand_hourly.csv")
    return demand_cph['demand_kwh']


def get_model_df(input_date):
    valid_date = parser.parse(input_date)

    price_cph = get_price_output(valid_date.strftime('%Y-%m-%d'))
    battery_cph = get_battery_output(valid_date.timetuple().tm_yday)
    demand_cph = get_demand_output()
    # pv_cph = get_pv_output()

    df = pd.DataFrame({'battery_cph': battery_cph,
                       'price_cph': price_cph,
                       'demand_cph': demand_cph})
                       # 'pv_out_cph': pv_cph})
    df['demand_cph'] = df['demand_cph'] * 10
    # df['pv_out_cph'] = df['pv_out_cph'] * 20 / 250
    return df

app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='SunDial - solar energy cost optimization analysis'),
    html.Div(children=[
        html.H2("Date"),
        dcc.DatePickerSingle(id="date-picker", date=dt(2016, 1, 5))
    ]),
    html.Button('Sumbit', id="submit-button"),

    dcc.Graph(id='model-graphs'),

    dcc.Graph(id='optimizer-graph')
])

@app.callback(
    Output('model-graphs', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('date-picker', 'date')]
)
def update_model_div(_, input_date):
    model_output_df = get_model_df(input_date)
    x = [i for i in range(24)]

    fig = tools.make_subplots(rows=3, cols=1, vertical_spacing=0.2, subplot_titles=model_output_df.columns.values)
    for i, column_name in enumerate(model_output_df.columns.values):
        trace = go.Scatter(
            x=x,
            y=model_output_df[column_name],
            mode="lines+markers",
            name=column_name
        )

        fig.append_trace(trace, i + 1, 1)
    return fig


# @app.callback(
#     Output('optimizer-graph', 'figure'),
#     [Input('submit-button', 'n_clicks')],
#     [State('date-picker', 'date')]
# )
# def update_optimizer_div():

# print(dcc.Input)

if __name__ == '__main__':
    app.run_server()