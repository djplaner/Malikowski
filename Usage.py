#
# Usage.py
# - Calculates Malikowski categories for a given set of courses
# - Does this using student clicks

#from Malikowski import Indicators
from Malikowski.Adoption import Adoption
import pandas as pd

query = """
select 
  courseid as course,shortname,fullname,component as name,sum(clicks) as x
from 
  {mav_prefix}logstore_standard_log, {mdl_prefix}course as c
where
  courseid in ( {courses}) and c.id=courseid
group by 
  course,shortname,fullname,component
"""

#- SQL to get course details for all matching a given shortname using like

shortnameQuery = """
select 
  courseid as course,shortname,fullname,component as name,sum(clicks) as x
from 
  {mav_prefix}logstore_standard_log, {mdl_prefix}course as c
where
  shortname like '{shortname}' and c.id=courseid
group by 
  course,shortname,fullname,component
"""

class Usage(Adoption):
    """Generate original Malikowski model by counting student clicks

    Attributes:
        df: raw data frame containing the adoption data for each course
        malikowski: data frame with rows for each course
            multiindex course/shortname/fullname 
            and fields for each category

        engine: data base "engine"
        configuration: local configuration file
        prefix: moodle/database prefix
    """            

#    allCategories=['content','communication','assessment','evaluation','cbi']
   

    def __init__(self,title=""):
        Adoption.__init__(self,title)

        self.query = query
        self.shortnameQuery = shortnameQuery
        self.mapping = self.configuration['usageMappingMAV']
        
    def clicksPerStudent(self):
        """ Modify the raw number of clicks to clicks per enrolled student"""
        for index,row in self.malikowski.iterrows():
            course = row['course']
            # get the matching TOTAL number of students from self.students
            # - total is 0 if no students
            total=0
            if ( self.students['course'] == course ).any():
                total = self.students['TOTAL'].loc[
                        self.students['course'] == course].values[0]

            # for each of the malikowski categories, 
            # divide the count by the total number of students
            for category in self.allCategories:
                raw = self.malikowski.loc[index, category]
                self.malikowski.loc[index, category] = 0
                if total != 0: 
                    self.malikowski.loc[index, category] = raw / total;

