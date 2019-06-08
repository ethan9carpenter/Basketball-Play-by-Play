import pandas as pd

def apply_grouping(df, grouping):   
    """ 
    grouping : array-like
        ('PlayerName', 'EventType', 'isAssisted', 'assistPlayerID', 'TeamName') 
    """ 
    #grouping = grouping.isin(self.columns)
    
    grouped = df.groupby(grouping)
    
    mean = pd.DataFrame(grouped.mean()['PointValue_sbsq'])
    mean.columns = ['AveragePoints']
    
    count = pd.DataFrame(grouped.count()['PointValue_sbsq'])
    count.columns = ['Count']
    
    return mean.join(count)