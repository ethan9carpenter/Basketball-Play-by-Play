import dash_core_components as dcc
from dash_daq import BooleanSwitch

_generic_dropdown = {'value': [],
                    'multi': True,
                    'style': {'font-size': 20}}

def _dropdown(**kwargs):
    return dcc.Dropdown(**{**kwargs, **_generic_dropdown})

class VisualComponents():
    def __init__(self, df):
        self.df = df

    @property
    def playerFilter(self):
        if not hasattr(self, '_playerFilter'):
            options = [{'label': name+' ({})'.format(team), 
                          'value': id_} for name, team, id_ in zip(self.df['PlayerName'],
                                                                   self.df['TeamName'],
                                                                   self.df['EventPlayerID'])]
            self._playerFilter = _dropdown(options=options, id='player-filter')
        return self._playerFilter
    
    @property
    def teamFilter(self):
        if not hasattr(self, '_teamFilter'):
            options=[{'label': i, 'value': i} for i in sorted(self.df['TeamName'].unique())]
            self._teamFilter = _dropdown(options=options, id='team-filter')
        return self._teamFilter
    
    @property
    def eventTypeFilter(self):
        if not hasattr(self, '_eventTypeFilter'):
            options=[{'label': i, 'value': i} for i in sorted(self.df['EventType'].unique())]
            self._eventTypeFilter = _dropdown(options=options, id='event-type-filter')
            
        return self._eventTypeFilter
    
    @property
    def isRelativeSwitch(self):
        if not hasattr(self, '_isRelativeSwitch'):
            self._isRelativeSwitch = BooleanSwitch(
                        id='isRelative',
                        on=True,
                        label='Display Relative Values',
                        style={'float': 'left'}
                        )
        return self._isRelativeSwitch
    
    @property
    def isChartSwitch(self):
        if not hasattr(self, '_isChartSwitch'):
            self._isChartSwitch = BooleanSwitch(
                        id='isChart',
                        on=True,
                        label='Chart',
                        style={'float': 'left'}
                    )
        return self._isChartSwitch