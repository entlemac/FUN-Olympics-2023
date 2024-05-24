from dash import Dash, html, dcc, Input, Output, callback_context
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data
data = pd.read_csv('FUNOlympics2023.csv')

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1('FUNOLYMPIC GAMES 2023  DASHBOARD', style={'text-align': 'center', 'color': 'white', 'background-color': 'darkgrey'}),
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavLink("Pie Chart", id="pie-chart-link", href="#", active=True, className="grey-button"),
                    dbc.NavLink("Bar Chart", id="bar-chart-link", href="#", className="grey-button"),
                    dbc.NavLink("Histogram", id="histogram-link", href="#", className="grey-button"),
                    dbc.NavLink("Map", id="map-link", href="#", className="grey-button"),
                ], vertical=True, pills=True, className="bg-light"),
            ], width=2),
            dbc.Col([
                html.Div(id='graph-content', className='container', style={'background-color': 'lightgrey', 'padding': '20px'})
            ], width=10)
        ]),
    ])
])

# Define callback functions to update graph content
@app.callback(
    Output('graph-content', 'children'),
    [Input('pie-chart-link', 'n_clicks'),
     Input('bar-chart-link', 'n_clicks'),
     Input('histogram-link', 'n_clicks'),
     Input('map-link', 'n_clicks')]
)
def render_content(pie_clicks, bar_clicks, hist_clicks, map_clicks):
    ctx = callback_context
    if not ctx.triggered:
        tab = 'pie-chart-tab'
    else:
        tab = ctx.triggered[0]['prop_id'].split('.')[0]
    if tab == 'pie-chart-link':
        return html.Div([
            dcc.Dropdown(id='country-dropdown', options=[{'label': i, 'value': i} for i in data['Countries'].unique()], value='United States'),
            dcc.Graph(id='pie-chart')
        ])
    elif tab == 'bar-chart-link':
        return html.Div([
            dcc.Dropdown(id='sport-dropdown-bar', options=[{'label': i, 'value': i} for i in data['Sports'].unique()], value='Athletics'),
            dcc.Dropdown(id='gender-dropdown-bar', options=[{'label': 'Male', 'value': 'Male'}, {'label': 'Female', 'value': 'Female'}], value='Male'),
            dcc.Graph(id='bar-chart')
        ])
    elif tab == 'histogram-link':
        return html.Div([
            dcc.Dropdown(id='sport-dropdown', options=[{'label': i, 'value': i} for i in data['Sports'].unique()], value='Athletics'),
            dcc.Graph(id='histogram')
        ])
    elif tab == 'map-link':
        return html.Div([
            dcc.Dropdown(id='map-country-dropdown', options=[{'label': i, 'value': i} for i in data['Countries'].unique()], value='United States'),
            dcc.Graph(id='map')
        ])

# Define callback functions for graph updates
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_pie_chart(country):
    sport_data = data[data['Countries'] == country]
    pie_fig = px.pie(sport_data, values='Viewership', names='Sports', color='Sports', color_discrete_sequence=px.colors.sequential.Rainbow)
    pie_fig.update_layout(title=f'Distribution of Viewership by Sport in {country}')
    return pie_fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('sport-dropdown-bar', 'value'),
     Input('gender-dropdown-bar', 'value')]
)
def update_bar(selected_sport, selected_gender):
    filtered_data = data[(data['Sports'] == selected_sport) & (data['Gender'] == selected_gender)]
    grouped_data = filtered_data.groupby('Countries', as_index=False).agg({'Viewership': 'sum'})
    updated_figure = px.bar(grouped_data, x="Countries", y="Viewership", barmode="group", title=f'Viewership for {selected_sport} by {selected_gender}')
    return updated_figure

@app.callback(
    Output('histogram', 'figure'),
    [Input('sport-dropdown', 'value')]
)
def update_histogram(sport):
    sport_data = data[data['Sports'] == sport]
    hist_fig = px.histogram(
        sport_data, 
        x='Countries', 
        y='Viewership', 
        color='Gender', 
        barmode='group', 
        histfunc='sum'
    )
    hist_fig.update_layout(title=f'Total Viewership by Country and Gender for {sport}')
    return hist_fig

@app.callback(
    Output('map', 'figure'),
    [Input('map-country-dropdown', 'value')]
)
def update_map(country):
    country_data = data[data['Countries'] == country]
    fig = px.choropleth(country_data, locations='Countries', locationmode='country names', color='Visits', hover_name='Countries', projection='natural earth', title=f'Distribution of Site Visits in {country}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
