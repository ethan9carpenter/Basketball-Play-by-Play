import pandas as pd
from collections import Counter, OrderedDict
import numpy as np
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output
import plotly.offline as py


df = pd.read_csv('2017-18_pbp.csv')
df = df.set_index('EVENTNUM')
df.sort_index(inplace=True)

df.sort_index(inplace=True)

sequences = pd.DataFrame(df['EVENTMSGACTIONTYPE'])
sequences.columns = ['p1']
sequences['p2'] = sequences['p1'].shift(1)
sequences.dropna(inplace=True)


sank = pd.DataFrame(columns=['first', 'second', 'count', 'color'])
pairs = list(zip(sequences['p1'], sequences['p2']))
counts = OrderedDict(Counter(pairs))
pairs = list(counts.keys())
first = [pair[0] for pair in pairs]
second = [pair[1] for pair in pairs]
counts = counts.values()


sank['first'] = np.array(first)
sank['first'] = sank['first'].astype(int)
sank['second'] = second
sank['second'] = sank['second'].astype(int)
sank['second'] = sank['second'] + 1000
sank['count'] = counts
#sank['color'] = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']
#sank['label'] = ['make', 'miss', 'make', 'miss']

data = dict(
    type='sankey',
    domain = dict(
      x =  [0,1],
      y =  [0,1]
    ),
    orientation = "h",
    valueformat = ".0f",
    node = dict(
      pad = 10,
      thickness = 30,
      line = dict(
        color = "black",
        width = 0
      ),
      #label =  sank['label'],
      #color = sank['color']
    ),
    link = dict(
      source = sank['first'].dropna(axis=0, how='any'),
      target = sank['second'].dropna(axis=0, how='any'),
      value = sank['count'].dropna(axis=0, how='any'),
      #color = sank['color'].dropna(axis=0, how='any'),
  )
)
layout = go.Layout(
    title=go.layout.Title(
        text='Three Point Attemps',
        xref='paper',
        x=0
    )
)

fig = dict(data=[data], layout=layout)
app = dash.Dash(__name__)
app.layout = html.Div([
            dcc.Graph(id='graph', animate=True)
            ]
    )

@app.callback(Output(component_id='graph', component_property='figure'))
def update_graph_scatter():
    return {'data': [data],
            'layout' : layout
            }


if __name__ == '__main__':
    app.run_server(debug=True)
    #py.plot(fig, auto_open=True)