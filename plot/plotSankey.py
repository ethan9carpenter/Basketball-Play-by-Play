from collections import Counter, OrderedDict
import numpy as np
import plotly.graph_objs as go
import pandas as pd

def _cat_to_num(data):    
    playTypes = set(data)
    key = zip(dict(Counter(data)).keys(), 
              list(range(len(playTypes))))
    key = dict(key)
    
    data = [key[val] for val in data]
    data = pd.Series(data)
    
    return data, key

class Sankey():
    def __init__(self, data, length=2):
        self.length = length
        self.plotDF = self._to_sankey_df(data, length)
        self.fig = self._to_sankey_plot(df=self.plotDF)
        
    def _to_sankey_df(self, data, length, dropna=True):
        data, key = _cat_to_num(data)
        
        df = pd.DataFrame()
        
        
        for i in range(length-1):
            newDF = pd.DataFrame({'source': data.shift(i+1) + 1000 * i,
                                  'target': data.shift(i) + 1000 * (i + 1)})
            df = pd.concat([df, newDF])
            
        if dropna:
            df.dropna(inplace=True)
        
    
        sank = pd.DataFrame(columns=['source', 'target', 'count'])
        pairs = list(zip(df['source'], df['target']))
        counts = OrderedDict(Counter(pairs))
        pairs = list(counts.keys())
        source = [pair[0] for pair in pairs]
        target = [pair[1] for pair in pairs]
        counts = counts.values()
    
        sank['source'] = np.array(source)
        sank['target'] = target
        sank['count'] = counts
        
        sank['source'] = (sank['source'] / 1000).astype(int)*len(key)+sank['source'] % 1000
        sank['target'] = (sank['target'] / 1000).astype(int)*len(key)+sank['target'] % 1000
        
        self.key = key
        self.numNodes = len(key)
        #print(sank)
        return sank
    
    def _to_sankey_plot(self, source=None, target=None, df=None):
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
              label = list(self.key.keys()) * self.length

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