#
# AdoptionView.py
# - simple test for a view

import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

class AdoptionView:
    """Take a Adoption object and generate a plot"""
   
    def __init__(self,adoption):
        self.model = adoption

    def stackedBar(self ):
        """plot it"""

        #-- drop some columns
        df = self.model.malikowski.drop(
                self.model.malikowski.columns[[0,2]],axis=1)

        #-- construct the bard
        trace1 = go.Bar( x=df.shortname, y=df.content, 
                         name='Content')
        trace2 = go.Bar( x= df.shortname, y= df.communication,
                        name='Communication')
        trace3 = go.Bar( x= df.shortname, y= df.assessment,
                        name='Assessment')
        trace4 = go.Bar( x= df.shortname, y= df.evaluation,
                        name='Evaluation')
        trace5 = go.Bar( x= df.shortname, y= df.cbi,
                        name='CBI')

        data = [trace1, trace2, trace3, trace4, trace5]
        layout = go.Layout( barmode='stack')

        fig = go.Figure( data=data, layout=layout)
        iplot( fig)
