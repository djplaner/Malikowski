#
# Usage.py
# - Calculates Malikowski categories for a given set of courses
# - Does this using student clicks

#from Malikowski import Indicators
from Malikowski.Adoption import Adoption
import pandas as pd

query = """
select 
    l.courseid as course,shortname,fullname,component as name,count(l.id) as x
from 
    {mdl_prefix}logstore_standard_log as l, {mdl_prefix}course as c
where 
    courseid in ( {courses} ) and c.id=courseid and userid in (
        select userid from moodle.mdl_role_assignments where roleid = '5' 
            and contextid in (
                select id from moodle.mdl_context where contextlevel='50' 
                    and instanceid = courseid ))
group by l.courseid,shortname,fullname,component
"""

#- SQL to get course details for all matching a given shortname using like

shortnameQuery = """
select 
    l.courseid as course,shortname,fullname,component as name,count(l.id) as x
from 
    {mdl_prefix}logstore_standard_log as l, {mdl_prefix}course as c
where 
    shortname like '{shortname}' and c.id=courseid and userid in (
        select userid from {mdl_prefix}role_assignments where roleid = '5' 
            and contextid in (
            select id from {mdl_prefix}context where contextlevel='50' 
                and instanceid = courseid ))
group by l.courseid,shortname,fullname,component
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
        self.mapping = self.configuration['usageMapping']



        
