import pandas as pd

class DataToAnalyze(pd.DataFrame):
    def apply_grouping(self, grouping):   
        """ 
        grouping : array-like
            ('PlayerName', 'EventType', 'isAssisted', 'assistPlayerID', 'TeamName') 
        """ 
        grouped = self.groupby(grouping)
        
        mean = pd.DataFrame(grouped.mean()['PointValue_sbsq'])
        mean.columns = ['AveragePoints']
        
        count = pd.DataFrame(grouped.count()['PointValue_sbsq'])
        count.columns = ['Count']
        
        return mean.join(count)