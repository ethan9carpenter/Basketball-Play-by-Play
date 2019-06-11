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
import warnings

warnings.filterwarnings('ignore')

conn = sql.connect("ncaa_pbp.db")
df = load_clean(2012, conn, limit='')
df = analysis.prep(df)

df = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'EventType', 'PointValue_sbsq']]

groupingCols = ['EventPlayerID', 'TeamID', 'EventType', 'PlayerName', 'TeamName']
labelCols = ['PlayerName', 'EventType']

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
                options=[{'label': i, 'value': i} for i in sorted(df['TeamName'].unique())],
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
                height=600
                )
            }

def get_team_names():
    return sorted(df['TeamName'].unique())



@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('player-filter', 'value'), 
     dash.dependencies.Input('isRelative', 'value')])
def update_graph(players, isRelative):    
    if players == []:
        return getEmptyChart()
 
    players = sorted(players)
    
    data = df[df['EventPlayerID'].isin(players)]
    
    count = data['Count']
    avg = data['AveragePoints']
    #text = [name + ' ({})'.format(event) for name, event in zip(data['PlayerName'], data['EventType'])]
    text = [name + ' ({})'.format(event) for name, event in zip(*[data[col] for col in labelCols])]
    
    yTitle = 'Points per Possession'

    if isRelative == 'yes':
        avg = avg - data['TeamAvg']
        yTitle += ' (Relative to Team Average)'


    return {
        'data': [go.Scatter(
            x=count,
            y=avg.values,
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
        teams = get_team_names()
    
    players = df[df['TeamName'].isin(teams)][['PlayerName', 'TeamName', 'EventPlayerID']]
    players.sort_values('PlayerName', inplace=True)
    players.drop_duplicates(inplace=True)
    
    options = [{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(players['PlayerName'],
                                                                   players['TeamName'],
                                                                   players['EventPlayerID'])]

    return  options


if __name__ == '__main__':
    app.run_server(debug=True)