#
# StudentsInCourses.py
# - given a list of course ids, identify the total # of students plus
#   counts of different types

from Malikowski import Indicators

import pandas as pd

query = """
select 
    courseid,name,count(userid)
from 
    {mdl_prefix}groups as groups,{mdl_prefix}groups_members as members
where 
    groups.id=groupid and courseid in ( {courses} ) and 
    ( name like 'On-Campus%' or name like 'Online%' )
group by courseid,name
"""

class StudentsInCourses:
    """Use query to get list of students by groups and then manipulate that into
    a single data frame (Studs) with x as total and then other columns based on 
    groupnames"""

    def __init__(self, courses):
        self.df = None

        self.courses = courses

        #-- site specific stuff
        # - database engine
        self.engine = Indicators.connect()

        # - configuration
        self.configuration = Indicators.config()
        self.mdl_prefix = self.configuration['mdl_prefix']  
        self.mav_prefix = self.configuration['mav_prefix']  
        self.mapping = self.configuration['adoptionMapping']
        self.query = self.configuration['StudentsInCourses']


    def getData(self ):
        """run the query"""

        #-- create string list of course ids
        inCourses = ','.join(map(str,self.courses))
        q = self.query.format( courses=inCourses, mdl_prefix=self.mdl_prefix,
                               mav_prefix=self.mav_prefix )

        #-- get the data
        self.df = pd.read_sql(q,self.engine)

        #-- post process into final df
        self.createStuds()
#        self.addPercentageAdoption()

    def createStuds(self):
        """create data frame row = course, columns is total counts for 
        different student types, including TOTAL"""

        # turn separate rows into a single based on course
        tmp = self.df.pivot_table( 'count',['course'],'name')
        tmp.reset_index( drop=False,inplace=True)

        tmp = tmp.fillna(0)
        # calculate the total number of students
        col_list = list(tmp)
        col_list.remove('course')
        tmp['TOTAL'] = tmp[col_list].sum(axis=1)

        self.Studs = tmp;

