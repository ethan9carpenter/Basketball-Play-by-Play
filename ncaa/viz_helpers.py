import plotly.graph_objs as go

def build_scatter(df, players, isRelative, labelCols):
    if players == []:
        return getEmptyChart()
 
    players = sorted(players)
    
    data = df[df['EventPlayerID'].isin(players)]
    
    count = data['Count']
    avg = data['AveragePoints']
    #text = [name + ' ({})'.format(event) for name, event in zip(data['PlayerName'], data['EventType'])]
    text = [name + ' ({})'.format(event) for name, event in zip(*[data[col] for col in labelCols])]
    
    yTitle = 'Points per Possession'

    if isRelative:
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

def getEmptyChart():
    return {'layout': go.Layout(
                title={'text': 'Average Points on Play after Player ends Possession'},
                xaxis={'title': 'Count'},
                yaxis={'title': 'Points per Possession'},
                height=600
                )
            }