from collections import Counter, OrderedDict
import numpy as np
import plotly.graph_objs as go
import pandas as pd

def _cat_to_num(source, target, circular=False):
    data = list(source) + list(target)
    
    playTypes = set(data)
    key = zip(OrderedDict(Counter(data)).keys(), 
              list(range(len(playTypes))))
    key = OrderedDict(key)
    
    source = [key[val] for val in source]
    target = [key[val]+len(playTypes) if not circular else 0 for val in target]
    
    return source, target, key



class Sankey():
    def __init__(self, source, target):
        self.plotDF = self.to_sankey_df(source, target)
        self.fig = self.to_sankey_plot(df=self.plotDF)
        
    def to_sankey_df(self, source, target, circular=False):
        source, target, key = _cat_to_num(source, target)
        
        df = pd.DataFrame()
        df['source'] = source
        df['target'] = target
    
        sank = pd.DataFrame(columns=['source', 'target', 'count'])
        pairs = list(zip(df['source'], df['target']))
        counts = OrderedDict(Counter(pairs))
        pairs = list(counts.keys())
        source = [pair[0] for pair in pairs]
        target = [pair[1] for pair in pairs]
        counts = counts.values()
    
    
        sank['source'] = np.array(source)
        sank['source'] = sank['source']
        sank['target'] = target
        sank['target'] = sank['target']
        sank['target'] = sank['target']
        sank['count'] = counts
        
        self.key = key
        
        return sank
    
    def to_sankey_plot(self, source=None, target=None, df=None):
        if source is not None and target is not None:
            df = self.to_sankey_df(source, target)
        
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
              label = list(self.key.keys()) * 2

            ),
            link = dict(
              source = df['source'].dropna(axis=0, how='any'),
              target = df['target'].dropna(axis=0, how='any'),
              value = df['count'].dropna(axis=0, how='any')
          )
        )
        layout = go.Layout()
        
        fig = dict(data=[data], layout=layout)
        
        return fig