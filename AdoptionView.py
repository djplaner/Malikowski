#
# AdoptionView.py
# - simple test for a view

import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from plotly.graph_objs import *

class AdoptionView:
    """Take a Adoption object and generate a plot"""
   
    def __init__(self,adoption=None):
        self.model = adoption
    
        #-- booleans used to indicate if (n=) has been added to title
        self.studentsAdded = False
        self.coursesAdded = False

    def stackedBar(self ):
        """plot it"""

        # add (n=??) if we have students
        if not self.studentsAdded and self.model.students is not None:
            self.addTotalStudents()

        ## TODO: return if model is NONE
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

        # add (n=??) if we have students
        if not self.studentsAdded and self.model.students is not None:
            self.addTotalStudents()

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

        ## TODO: return if model is NONE

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
    

    def listCategoryComparison(self, groups, showCategories=None):
        """Groups contains a list of Adoption models (typically for groups of 
        courses. Show one box plot for each category comparing each of the
        groups of courses.
        - showCategories is a dict with keys matching category names, only show
          included categories """

        #-- TODO: check to make sure the list isn't empty

        #-- get list of all Malikowski categories
        allCategories = groups[0].allCategories;

        #-- create graph for each category
        for category in allCategories:

            if showCategories is not None and not category in showCategories:
                continue
            #-- place the Box for each group of courses
            data = []
            #-- generate the Box for each group of courses
            for group in groups:
                if not self.coursesAdded:
                    numCourses = len(group.malikowski.index)
                    group.title += " (n=" + str(numCourses) + ")"

                #-- tmp pointer to malikoski data frame
                temp = group.malikowski
                #-- get the slice of the dataframe by the variable name category
                y = getattr( temp, category)
                title = group.title # group.title.replace( " ", "_" )
                box = go.Box( y=y, name=title, boxpoints='all')
                data.append(box)

            self.coursesAdded = True
            #-- draw the graph for the category
            layout = go.Layout( title=category)
            fig = go.Figure( data=data, layout=layout)
            iplot(fig)

    def listCategoryPercentage( self, groups, showCategories=None):
        """create one graph per category and show the percentage adoption 
        for each group of courses. But only for categories in showCategories"""

        #-- TODO: check to make sure the list isn't empty

        allCategories = groups[0].allCategories;

        for category in allCategories:
            if showCategories is not None and not category in showCategories:
                continue
            x = []
            y = []
            mMin = []
            mMax = []
    
            malikowskiMin = {'content':50, 'communication':20, 'assessment':20, 'evaluation':0, 'cbi':0}
            malikowskiMax = {'content':100, 'communication':50, 'assessment':50, 'evaluation':20, 'cbi':10}
            for group in groups:
                if not self.coursesAdded:
                    numCourses = len(group.malikowski.index)
                    group.title += " (n=" + str(numCourses) + ")"

                x.append(group.title)
                y.append(group.percentages[category])
                mMin.append(malikowskiMin[category])
                mMax.append(malikowskiMax[category])

            self.coursesAdded = True

            bar = go.Bar( y=y, x=x, opacity=0.8,name="% course adoption" )
            trace1 = go.Scatter(x=x,y=mMin, name="Malikowski min. %",
                                        mode="lines")
            trace2 = go.Scatter(x=x,y=mMax, name="Malikowski max. %",
                                    mode="lines")
            data = [bar,trace1,trace2]

    
            layout = go.Layout( title=category,yaxis=YAxis( title="% courses", 
                                range=[0,100]), xaxis=XAxis( title="Terms"))
            fig = go.Figure( data=data, layout=layout)
            iplot(fig)

    def addTotalStudents(self):
        self.studentsAdded = True
        for index,row in self.model.malikowski.iterrows():
            # get the course
            course = row['course']
            shortname = row['shortname']
            # find TOTAL in students matching course
            total = self.model.students['TOTAL'].loc[ 
                        self.model.students['course'] == course].values[0]

            newName = "{name}\n (n={n:.0f})".format(name=shortname,n=total)
            self.model.malikowski.loc[index,'shortname'] = newName

