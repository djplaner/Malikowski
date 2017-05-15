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
        width = len(df.index) * 30
        if width < 500:
            width = 500
        layout = go.Layout( barmode='stack', width=width)

        fig = go.Figure( data=data, layout=layout)
        iplot( fig)


    def stackedBarHorizontal(self ):
        """plot horizontally a stacked bar chart - 1 bar per course"""

        #-- drop some columns
        df = self.model.malikowski.drop(
                self.model.malikowski.columns[[0,2]],axis=1)

        #-- construct the bard
        trace1 = go.Bar( y=df.shortname, x=df.content,
                         name='Content', orientation ='h')
        trace2 = go.Bar( y= df.shortname, x= df.communication,
                        name='Communication', orientation ='h')
        trace3 = go.Bar( y= df.shortname, x= df.assessment,
                        name='Assessment', orientation ='h')
        trace4 = go.Bar( y= df.shortname, x= df.evaluation,
                        name='Evaluation', orientation ='h')
        trace5 = go.Bar( y= df.shortname, x= df.cbi,
                        name='CBI', orientation ='h')

        data = [trace1, trace2, trace3, trace4, trace5]

        height = len(df.index) * 50
        if height < 600:
            height = 600
        layout = go.Layout( barmode='stack', 
                        height=height,
                        title="All courses",
                        margin = go.Margin( l=150, r=50, b=100, t=100, pad=4) )

        fig = go.Figure( data=data, layout=layout)
        iplot( fig)

    def boxPlotComparison(self, title):
        """Show a box plot comparison for each Malikowski category for
        all the courses in the current model"""

        model = self.model
        numCourses = len(model.malikowski.index)
        title += ' (n=' + str(numCourses) + ')'

        #-- set up each of the bars - 1 per Malikowski category
        content = go.Box( y=model.malikowski.content, name='Content',
                            boxpoints='all',boxmean='sd')
        communication = go.Box( y=model.malikowski.communication,   
                                name='Communication', boxpoints='all')
        assessment = go.Box( y=model.malikowski.assessment, 
                            name='Assessment',boxpoints='all')
        evaluation = go.Box( y=model.malikowski.evaluation, name='Evaluation',
                            boxpoints='all')
        cbi = go.Box( y=model.malikowski.cbi, name='cbi',boxpoints='all')

        layout = go.Layout( title=title)

        data = [ content, communication, assessment, evaluation, cbi]
        fig = go.Figure( data=data, layout=layout)
        iplot(fig)
    
