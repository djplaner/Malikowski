#
# Adoption.py
# - Calculates Malikowski categories for a given set of courses
# - Uses very simple presence of features in course_module table NOT usage

from Malikowski import Indicators
import pandas as pd

query = """
select 
    course,shortname,fullname,name,count(cm.id) x 
from 
    {mdl_prefix}course_modules as cm,{mdl_prefix}modules as m,{mdl_prefix}course as c
where 
    course in ( {courses} ) and module=m.id and c.id=course 
group by course,shortname,fullname,name order by course
"""

# USQ mapping 2015

mapping = { 'spider' : 'unknown',
'smarthinking' : 'communication',
'usqvideo' : 'content',
'turnitintooltwo' : 'assessment',
'lightboxgallery' : 'content',
'voiceauthoring': 'content',
'voiceboard' : 'communication',
'voiceemail' : 'communication',
'voicepodcaster': 'content',
'voicepresentation': 'content',
'engagement' : 'evaluation', #-- analytics - revaling about students
'book': 'content',
'choice' : 'evaluation',
'data' : 'content', #--questionable could be communication??
'elluminate' : 'communication',
'usqnavicons': 'content',
'equella': 'content',
'feedback' : 'evaluation',
'folder': 'content',
'glossary': 'content',
'imscp' : 'content',
'label' : 'content',
'lesson' : 'cbi',
'lti' : 'unknown', #-- could be anything, depending on what is pointed to
'page': 'content',
'resource': 'content',
'survey' : 'evaluation',
'url': 'content',
'wiki' : 'communication', #-- questionable
'scorm': 'content',
'dialogue' : 'communication',
'forum' : 'communication',
'voicetools' : 'content',
'assignment' : 'assessment',
'liveclassroom' : 'communication',
'usqease' : 'assessment',  #-- questionable - also gradebook
'usqgetstarted' : 'content',
'chat' : 'communication',
'assign': 'assessment', #-- questionable - also grades
'quiz': 'assessment',
'workshop' : 'assessment',
'bim' : 'communication', #-- questionable
};


class Adoption:
    """Generate original Malikowski model using simple presence/adoption of 
    features. Do so for a list of courses specific either by list of ids/period

    Attributes:
        df: raw data frame containing the adoption data for each course
        malikowskiCourseDF: conversion into Malikowski
        engine: data base "engine"
        configuration: local configuration file
        prefix: moodle/database prefix
    """            

    allCategories=['content','communication','assessment','evaluation','cbi']
   
    def __init__(self):
        self.df = "hello"
        self.engine = Indicators.connect()
        self.configuration = Indicators.config()

        self.prefix = self.configuration['mdl_prefix']  

    def getCourses(self, courses ):
        """Return Malikowski model array for each course. Use simple adoption
        taken from course_modules"""
        if not courses:
            print ("No courses specified")
            return;

        #-- create string list of course ids
        inCourses = ','.join(map(str,courses))
        q = query.format( courses=inCourses, mdl_prefix=self.prefix )

        #-- get the data
        self.df = pd.read_sql(q,self.engine)

        #-- post process with malikowski stuff
        self.addMalikowskiColumn()
        self.createMalikowski()


    def addMalikowskiColumn(self):
        """add the column for malikowski translation to the df"""
        malikowskis = []
        for index, row in self.df.iterrows():
            malikowskis.append(mapping[row['name']]);
        self.df['malikowski'] = malikowskis;

    def createMalikowski(self):
        """create data frame row = course, columns is total counts for 
        Malikowski categories, including counts and percentages""" 
        #-- group all the malikowski categories together
        self.malikowskiGroup = self.df.groupby( 
           ['course','shortname','fullname','malikowski']).sum().reset_index()

##-- need to fill in the missing malikowski categories with 0s

        #-- calculate total feature adoption for the course
        #   - df courseid => total x
        total = self.malikowskiGroup.groupby(['course']).sum()

        #-- add a percentage and total column for each course
        percents = []
        for index, row in self.malikowskiGroup.iterrows():
            percent = row['x'] * ( 100 / total.loc[row['course']].x )
            p= "{0:.2f}".format(percent)
            percents.append( p);
        self.malikowskiGroup['percent'] = percents;

        self.malikowskiGroup = self.addMissingCategories(self.malikowskiGroup )

        #-- group all the course related data into a single row
        next = self.malikowskiGroup.pivot_table(
                    'x',['course','shortname','fullname'],'malikowski')
        next.reset_index(drop=False,inplace=True)
        self.malikowski = next

    def addMissingCategories(self,group):
        """Loop through malikowskiGroup dataframe and add 0x 0% rows
        for all malikowski categories that are missing for courses.
        i.e. ensure that all courses have data for all categories.
        - return group with missing categories appended """

        #***** TODO: should probably add error checking on group

        # list storing rows to add
        missing=[]

        #- get list of uniqe course ids
        courses = group.course.unique()

        #-- for each course 
        for course in courses:
            # get data frame with the present malikowski categories for the current course
            present=group.loc[group['course'] == course, 
                                    ['malikowski','shortname','fullname']]
            # grab the short/fullname
            shortName = present.iloc[0].shortname
            fullName = present.iloc[0].fullname
    
            # get a list of the malikowski categories for this course
            presentList = present['malikowski'].tolist()
    
            # get a list of categories not present for this course
            notThere = list(set(self.allCategories) - set(presentList))

            # add rows for missing categories
            for cat in notThere:
                row = { 'course':course,  'shortname':shortName, 
                        'fullname':fullName, 'malikowski':cat, 
                        'x':0, 'percent':0.0}
                missing.append( row)
            
        missingDF = pd.DataFrame(missing)
        group = group.append( missingDF )
        group.reset_index(drop=True,inplace=True)
        return group
 


        
