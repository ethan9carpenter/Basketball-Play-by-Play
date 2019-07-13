import dash
#https://dash.plot.ly/interactive-graphing
import dash_core_components as dcc
import dash_html_components as html
from dash_daq import BooleanSwitch
from dash.dependencies import Input, Output
from ncaa import analysis
from ncaa.load_data import load_clean
from ncaa.analysis.analyze import apply_grouping
import pandas as pd
import sqlite3 as sql
import warnings
from ncaa.viz_helpers import build_scatter, build_table, prepare_data_for_viz

warnings.filterwarnings('ignore')

conn = sql.connect("ncaa_pbp.db")
df = load_clean(2019, conn, limit=None)
df = analysis.prep(df)

df = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'EventType', 'PointValue_sbsq']]

labelCols = ['PlayerName']
groupingCols = ['EventPlayerID', 'TeamID', 'TeamName'] + labelCols


teamAvg = apply_grouping(df, ['TeamID'])['AveragePoints']
df = apply_grouping(df, groupingCols)

df.reset_index(inplace=True)
df = pd.merge(df, teamAvg.reset_index().rename({'AveragePoints': 'TeamAvg'}, axis=1), on='TeamID', how='left')


app = dash.Dash('NCAA Play-by-Play')

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='player-filter',
                options=[{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(df['PlayerName'],
                                                                   df['TeamName'],
                                                                   df['EventPlayerID'])],
                value=[],
                multi=True,
                style={'font-size': 20}
            ),
            BooleanSwitch(
                id='isRelative',
                on=True,
                label='Display Relative Values',
                style={'float': 'left'}
            ),
            BooleanSwitch(
                id='isChart',
                on=True,
                label='Chart',
                style={'float': 'left'}
            )
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': '50%'}),
        html.Div([
            dcc.Dropdown(
                id='team-filter',
                options=[{'label': i, 'value': i} for i in sorted(df['TeamName'].unique())],
                value=[],
                multi=True,
                style={'font-size': 20}
            ),
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': 'right'}),
    ]),
    html.Div(id='display'),
])


@app.callback(
    Output('display', 'children'),
    [Input('player-filter', 'value'), 
     Input('isRelative', 'on'),
     Input('isChart', 'on'),
     Input('team-filter', 'value')])
def update_graph(players, isRelative, isChart, teams):
    #if players == []:
        #players = list(df['PlayerName'])
    
    data = prepare_data_for_viz(df.copy(), players, isRelative, labelCols, teams)
    
    if isChart:
        return [build_scatter(data, isRelative, labelCols)]
    else:
        return [build_table(data, labelCols)]
    
    
    
@app.callback(
    Output('player-filter', 'options'),
    [Input('team-filter', 'value')])
def update_player_filter(teams):
    if teams == []:
        teams = sorted(df['TeamName'].unique())
    
    players = df[df['TeamName'].isin(teams)][['PlayerName', 'TeamName', 'EventPlayerID']]
    players.sort_values('PlayerName', inplace=True)
    players.drop_duplicates(inplace=True)
    
    options = [{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(players['PlayerName'],
                                                                   players['TeamName'],
                                                                   players['EventPlayerID'])]

    return  options

@app.callback(
    Output('isChart', 'label'),
    [Input('isChart', 'on')])
def is_chart_label_update(isChart):
    if isChart:
        return "Scatter Plot"
    else:
        return  "Table"


if __name__ == '__main__':
    app.run_server(debug=True)