# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from tabs import current
from tabs import parameters
from tabs import projection

# VARIABLES
# PwC colors
colors = {
    'PwCColor1': "#D04A02",
    'PwCColor2': "#EB8C00",
    'PwCColor3': "#FFB600",
    'PwCColor4': "#DB536A",
    'PwCColor5': "#E0301E",
    'PwCGrey1': "#7D7D7D",
    'PwCGrey2': "#DEDEDE"
}

Parameters = {
    'ICU_capacity': 2200,
    'ventilator_capacity': 2000,
    'avg_infection_rate_days': 12
}


# FUNCTIONS

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Covid-19 Dashboard"),
                    html.H6("Projection Reporting"),
                ],
            ),
            html.A(
                id="banner-logo",
                children=[
                    html.Img(id="logo", src=app.get_asset_url("PwC.png"))
                ],
                href="https://www.pwc.com",

            ),
        ],
    )


# Build tabs
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab-1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Parameter-tab",
                        label="Parameters Used",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Current-tab",
                        label="Current situation",
                        value="tab-2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Projection-tab",
                        label="Projection",
                        value="tab-3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    )
                ],
            )
        ],
    )


# Generate table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# Import the CSV files from https://epistat.wiv-isp.be/Covid/

df_sex = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv', sep=',', encoding='latin-1')
df_muni = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv', sep=',', encoding='latin-1')
df_muni_cum = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv', sep=',', encoding='latin-1')
df_hosp = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv', sep=',', encoding='latin-1')
df_mort = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv', sep=',', encoding='latin-1')
df_tests = pd.read_csv('https://epistat.sciensano.be/Data/COVID19BE_tests.csv', sep=',', encoding='latin-1')
df_params = pd.read_csv("./data/parameters.csv")

# Create HTML structure

# Import stylesheets
external_stylesheets = ['/assets/pwc.css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets
)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),

        dcc.Tabs(id="tabs", value='tab-1-example', children=[
            dcc.Tab(
                id="Parameter-tab",
                label="Parameters",
                value="tab-1",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                id="Current-tab",
                label="Current situation",
                value="tab-2",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                id="Projection-tab",
                label="Projection",
                value="tab-3",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
        ]),


        html.Div(id='tabs-content')

    ],
)


# CALLBACKS
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return parameters.tab_1_layout
    elif tab == 'tab-2':
        return current.tab_2_layout
    elif tab == 'tab-3':
        return projection.tab_3_layout


# Tab parameter callback
@app.callback(
    Output(component_id='projection-chart', component_property='figure'),
    [Input(component_id='my-date-picker-range', component_property='start-date'),
     Input(component_id='my-date-picker-range', component_property='end-date'),]
)

# Filter dataframe
# def update_chart(start_date, end_date):
#     projection.df_proj_view = projection.df_proj.loc[start_date: end_date]

# Tab current callback
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Tab projection callback
@app.callback(Output('page-3-content', 'children'),
              [Input('page-3-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
