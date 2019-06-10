import dash
#https://dash.plot.ly/interactive-graphing
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from ncaa import analysis
from ncaa.load_data import load_clean
from ncaa.analysis.analyze import apply_grouping
import pandas as pd

import sqlite3 as sql
conn = sql.connect("ncaa_pbp.db")
df = load_clean(2019, conn, limit='')
df = analysis.prep(df)
df = df[df['PlayerName'] != 'Team']

origDF = df.copy()

playerNames = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName']]
playerNames = playerNames.set_index('PlayerName')
teams = apply_grouping(df, ['TeamID'])['AveragePoints']

groupedDF = apply_grouping(df, ['PlayerName', 'TeamID'])
groupedDF['AveragePoints'] -= teams

teamNames = sorted(list(set(playerNames['TeamName'])))
playerNames = sorted(list(set(playerNames.index)))


app = dash.Dash('NCAA Play-by-Play')

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='player-filter',
                options=[{'label': i, 'value': i} for i in playerNames],
                value=playerNames[0],
                multi=True,
                style={'font-size': 20}
            ),
            dcc.RadioItems(
                id='isRelative',
                options=[{'label': 'Relative to Team', 'value': 'relative'},
                         {'label': 'Total', 'value': 'total'}],
                value='False',
            )
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': '50%'}),
        html.Div([
            dcc.Dropdown(
                id='team-filter',
                options=[{'label': i, 'value': i} for i in teamNames],
                value='',
                multi=True,
                style={'font-size': 20}
            ),
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': 'right'}),
    ]),
    html.Div([
        dcc.Graph(
            id='graph',
        )
    ]),
])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('player-filter', 'value'), 
     dash.dependencies.Input('team-filter', 'value'), 
     dash.dependencies.Input('isRelative', 'value')])
def update_graph(players, teams, isRelative):
    if isinstance(players, str):
        text = players
    else:
        text = groupedDF.loc[players].reset_index()['PlayerName']
        
    if teams == '':
        teams = teamNames
    
    count = groupedDF.loc[players]['Count']
    avg = groupedDF.loc[players]['AveragePoints']
    
    
    
    #if isRelative == 'relative':
        #y = y - teams.xs(player['TeamID'])

    return {
        'data': [go.Scatter(
            x=count,
            y=avg,
            text=text,
            mode='markers',
            marker = {'size': 25}
        )],
        'layout': go.Layout(
            title={'text': 'Average Points on Play after Player ends Possession'},
            xaxis={'title': 'Count',},
            yaxis={'title': 'Average Points Relative to Team Average'},
            hovermode='closest',
            height=600
        ),
    }
    
@app.callback(
    dash.dependencies.Output('player-filter', 'options'),
    [dash.dependencies.Input('team-filter', 'value')])
def update_player_filter(teams):    
    if teams == '':
        teams = teamNames
    elif isinstance(teams, str):
        teams = [teams]
    
    players = origDF[['PlayerName', 'TeamName']]
    players = players[players['TeamName'].isin(teams)]
    players = sorted(list(set(players['PlayerName'])))
    
    options = [{'label': i, 'value': i} for i in players]

    return  options


if __name__ == '__main__':
    app.run_server(debug=True)