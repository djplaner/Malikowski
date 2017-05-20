# Malikowski Output indicators

Malikowski et. al (2007) proposed a research model for exploring the use of learning management systems (aka course management systems) such as Blackboard, Moodle etc. This project is developing code to support exploration of whether or not the "Malikowski" model can be useful in the generation of *output indicators*. Output indicators are seen as some measure of the consequences of learning and teaching.

The idea is to be able to use the Malikowski model to get an indication of what has happened in a course. While such an indication will be inherently limited, it may be better than what is currently available.

Initially, this code will be designed to work with the Moodle LMS across different institutions. It will be tested across two institutions.

## Pre-requisites

- Python with misc. modules (e.g. database)
- Moodle database
> Currently this is only working with Moodle. Assumes you have a connection to it.

You might also like to use the Jupyter notebooks in [the Indicators repository](https://github.com/djplaner/Indicators), especially those in the OutputIndicators folder, which are use the Malikowski code.

## Configuration

You will also need to create two JSON configuration files in a folder outside of the Malikowski project.

### config.json

The configuration for the Moodle database connection. 

**Example**

```{
  "drivername": "postgresql",
  "database": "moodle_dbase",
  "username": "postgres",
  "host": "localhost",
  "port": "5432",
  "password": "SomePassword"
}```

### lms.json

Meant to configure various LMS specific information

**Example**

```{  
    "mdl_prefix" : "moodle.mdl_",
    "adoptionMapping" : {
            "spider" : "unknown", "smarthinking" : "communication",
            "usqvideo" : "content", "turnitintooltwo" : "assessment",
            "lightboxgallery" : "content", "voiceauthoring": "content" 
     },
    "usageMapping" : { "mod_survey" : "evaluation", "mod_folder" : "content",
            "mod_forum" : "communication", "mod_quiz" : "assessment",
            "mod_book" : "content", "mod_scorm" : "content",
}```

- `mdl_prefix` - specifies the prefix for your Moodle database table names
- `adoptionMapping` - maps Moodle course module names to Malikowski categories
> This will be slightly different for each Moodle install, depending on the Modules installed. We're happy to share an initial rough mapping.
- `usageMapping` - matched `component` field from `logstore_standard_log` table to Malikowski categories

## Examples

Our current model is that this code is used in Jupyter Notebooks to perform analysis. Some examples are available via [another repository](https://github.com/djplaner/Indicators), including

- [comparing strange courses](https://github.com/djplaner/Indicators/blob/master/OutputIndicators/Malikowski%20changes%20mapped%20against%20strange%20courses.ipynb)
> Closer to the actual use.
- [initial development](https://github.com/djplaner/Indicators/blob/master/OutputIndicators/Malikowski%20explorations.ipynb)
> Original development notebook.

(Both notebooks are missing content to maintain data privacy)

## References

Malikowski, S., Thompson, M., & Theis, J. (2007). A model for research into course management systems: bridging technology and learning theory. Journal of Educational Computing Research, 36(2), 149–173.
