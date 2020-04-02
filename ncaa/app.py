import dash
#https://dash.plot.ly/interactive-graphing
import dash_html_components as html
from dash.dependencies import Input, Output
from ncaa import analysis
from ncaa.load_data import load_clean
import sqlite3 as sql
import warnings
from ncaa.viz.charts import build_scatter, build_table, prepare_data_for_viz
from ncaa.viz import VisualComponents

warnings.filterwarnings('ignore')

#### Constants ###
power5 = ['acc', 'pac_twelve', 'big_ten', 'big_twelve', 'sec', 'big_east']
constantCols = ['EventPlayerID', 'TeamID', 'TeamName']
#### Settings ####
year = 2019
labelCols = ['PlayerName', 'EventType']
minCount = 50
conferences = ['acc']
colorCol = 'EventType'
#### Setup #######

conn = sql.connect("ncaa_pbp.db")
df = load_clean(year, conn, limit=None)
df = analysis.prep(df, year, conn)
df = analysis.visual_filters(df, minCount=minCount, labelCols=labelCols, conferences=conferences)

app = dash.Dash('NCAA Play-by-Play')

components = VisualComponents(df)

app.layout = html.Div([
    html.Div([
            components.playerFilter,
            components.isRelativeSwitch,
            components.isChartSwitch
        ],
        style={'display': 'inline-block', 'width': '50%', 'float': '50%'}),
    html.Div([
        components.teamFilter,
        components.eventTypeFilter],
        style={'display': 'inline-block', 'width': '50%', 'float': 'right'},
    ),
    html.Div(id='display')
])


@app.callback(
    Output('display', 'children'),
    [Input('player-filter', 'value'), 
     Input('isRelative', 'on'),
     Input('isChart', 'on'),
     Input('team-filter', 'value'),
     Input('event-type-filter', 'value')])
def update_graph(players, isRelative, isChart, teams, events):
    #if players == []:
        #players = list(df['PlayerName'])
    
    data = prepare_data_for_viz(df.copy(), players, isRelative, teams, events)
    
    if isChart:
        return [build_scatter(data, isRelative, labelCols, colorCol=colorCol)]
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
    return "Scatter Plot" if isChart else "Table"

if __name__ == '__main__':
    app.run_server(debug=True)