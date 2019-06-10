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
df = load_clean(2012, conn, limit='')
df = analysis.prep(df)
df = df[df['PlayerName'] != 'Team']

origDF = df.copy()


teamAvg = apply_grouping(df, ['TeamID'])['AveragePoints']

groupedDF = apply_grouping(df, ['EventPlayerID', 'TeamID'])
#groupedDF['AveragePoints'] -= teams

teamNames = sorted(list(set(origDF['TeamName'])))

playerNames = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName']]
playerNames.drop_duplicates(inplace=True)
playerNames.sort_values('PlayerName', inplace=True)

app = dash.Dash('NCAA Play-by-Play')

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='player-filter',
                options=[{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(playerNames['PlayerName'],
                                                                   playerNames['TeamName'],
                                                                   playerNames['EventPlayerID'])],
                value=[],
                multi=True,
                style={'font-size': 20}
            ),
            dcc.RadioItems(
                id='isRelative',
                options=[{'label': 'Relative to Team', 'value': 'yes'},
                         {'label': 'Total', 'value': 'no'}],
                value='yes',
            )
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': '50%'}),
        html.Div([
            dcc.Dropdown(
                id='team-filter',
                options=[{'label': i, 'value': i} for i in teamNames],
                value=[],
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


def getEmptyChart():
    return {'layout': go.Layout(
                title={'text': 'Average Points on Play after Player ends Possession'},
                xaxis={'title': 'Count'},
                yaxis={'title': 'Points per Possession'},
                hovermode='closest',
                height=600
                )
            }

def get_player_name(id_):
    return playerNames[playerNames['EventPlayerID'] == id_]['PlayerName'].values[0]

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('player-filter', 'value'), 
     dash.dependencies.Input('team-filter', 'value'), 
     dash.dependencies.Input('isRelative', 'value')])
def update_graph(players, teams, isRelative):
    if isinstance(players, str):
        text = players        
    elif players == []:
        return getEmptyChart()
    else:
        text = pd.Series(players).apply(get_player_name)
                
    if teams == '':
        teams = teamNames
    
    count = groupedDF.loc[players]['Count']
    avg = groupedDF.loc[players]['AveragePoints']

        
    
    if isRelative == 'yes':
        avg = avg - teamAvg
        yTitle = 'Points per Possession (Relative to Team Average)'
    else:
        yTitle = 'Points per Possession'


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
            xaxis={'title': 'Count'},
            yaxis={'title': yTitle,
                   'range': [min(0, min(avg))*1.1, max(0, max(avg))*1.1]},
            hovermode='closest',
            height=600
        ),
    }
    
@app.callback(
    dash.dependencies.Output('player-filter', 'options'),
    [dash.dependencies.Input('team-filter', 'value')])
def update_player_filter(teams):
    if teams == []:
        teams = teamNames
    
    players = origDF[['PlayerName', 'TeamName', 'EventPlayerID']]
    players = players[players['TeamName'].isin(teams)].sort_values('PlayerName')
    players.drop_duplicates(inplace=True)
    
    options = [{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(players['PlayerName'],
                                                                   players['TeamName'],
                                                                   players['EventPlayerID'])]

    return  options


if __name__ == '__main__':
    app.run_server(debug=True)