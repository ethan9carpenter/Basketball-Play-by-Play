import dash_core_components as dcc
import plotly.graph_objs as go
import dash_table

def build_scatter(df, isRelative, labelCols):
    count = df['Count']
    avg = df['AveragePoints']

    text = ['-'.join(info) for info in zip(*[df[col] for col in labelCols])]
    
    yTitle = 'Points per Possession'

    if isRelative:
        yTitle += ' (Relative to Team Average)'


    return dcc.Graph(
            id='graph',
            figure={
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
            })
    
def build_table(df, labelCols):
    df = df[labelCols+['TeamName', 'AveragePoints', 'Count']]
    
    
    df.sort_values('AveragePoints', inplace=True, ascending=False)
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df['index'] += 1
    df.rename({'PlayerName': 'Name',
               'TeamName': 'Team',
               'index': 'Rank'
               }, axis=1, inplace=True)
    
    
    return dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                sorting=True
            )
    
def prepare_data_for_viz(df, players, isRelative, labelCols, teams):
    players = sorted(players)
    
    if players == [] and teams == []:
        pass
    elif players == [] and teams != []:
        df = df[df['TeamName'].isin(teams)]
    else:
        df = df[df['EventPlayerID'].isin(players)]
        

    if isRelative:
        df['AveragePoints'] -= df['TeamAvg']
        
    df['AveragePoints'] = df['AveragePoints'].round(3)
        
    return df

def empty_table():
    pass

def getEmptyChart():
    return dcc.Graph(
                id='graph',
                figure={'layout': go.Layout(
                            title={'text': 'Average Points on Play after Player ends Possession'},
                            xaxis={'title': 'Count'},
                            yaxis={'title': 'Points per Possession'},
                            height=600
                            )
                        }
            )