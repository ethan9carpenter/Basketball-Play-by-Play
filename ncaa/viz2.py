import dash
#https://dash.plot.ly/interactive-graphing
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from ncaa import analysis
from ncaa.load_data import load_clean
from ncaa.analysis.analyze import apply_grouping
import pandas as pd

if __name__ == '__main__':
    import sqlite3 as sql
    conn = sql.connect("ncaa_pbp.db")
    df = load_clean(2019, conn, limit=1000)
    df = analysis.prep(df)
    df = df[df['PlayerName'] != 'Team']
    
    
    df = apply_grouping(df, ['PlayerName', 'EventType'])
    playerNames = set(df.index.get_level_values('PlayerName').values)


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')
    
app = dash.Dash()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='player-name-filter',
                options=[{'label': i, 'value': i} for i in playerNames],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='true-or-relative',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ]),
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('player-name-filter', 'value')])
def update_graph(xaxis_column_name):
    dff = df

    yaxis_column_name = 'Life expectancy at birth, total (years)'

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text='name',
            mode='markers'
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_column_name,},
            yaxis={'title': yaxis_column_name},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)