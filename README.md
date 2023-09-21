# Texas Essential Knowledge and Skills (TEKS) Parts of Speech Analysis
### Scraping and Part of Speech Analysis of the Texas Essential Knowledge and Skills (TEKS)

In this project, I am scraping the [TEKS website](https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=19&pt=2) for all subjects in grades 4-8. Then I will be conducting a part of speech analysis by finding the most common verbs across all grades and subjects. 

This is a volunteer project in support of [Celebrate Dyslexia](https://celebratedyslexia.org/), a non-profit organization in Texas. Their mission is to foster a community that celebrates, educates and empowers those with Dyslexia. With the results of this analysis, the team at Celebrate Dyslexia will be empowered to create a curriculum that supplements TEKS in order to better support children in grades 4-8 who have Dyslexia.

### Description of TEKS and structure of site

From the [Study of the Essential Knowledge and Skills and Assessment Instruments (2016)](https://tea.texas.gov/sites/default/files/TEKSandAssessmentStudy.pdf):

> Twenty years ago, the State of Texas began the process of implementing a comprehensive set of
curriculum standards to establish the educational requirements in each subject area. In 1995 SB 1
charged the SBOE with identifying the essential knowledge and skills of each subject of the required
curriculum (TEC §28.002(c)). After several years of work and study, in 1997 the SBOE approved the state
curriculum standards, known as the Texas Essential Knowledge and Skills, or TEKS. Those curriculum
standards were first implemented in classrooms across the state in the 1998-1999 school year.

> The TEKS describe what students should know and be able to do at the end of each grade level or
course. Student expectations (SEs) identify the specific knowledge and skills that students must
demonstrate. Certain subject areas include SEs that focus on process skills. Process skills describe ways
in which students are expected to engage with the content. Mathematics, science, and social studies all
include SEs that focus on processes.

#### Site Description

The TEKS is outlined in [Title 19, Part 2 of the Texas Administrative Code](https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=19&pt=2). Chapters 110-130 cover each of the subject areas for the TEKS. Within each Chapter are Rules, which is where we find the TEKS statements for a single grade and subject (located at subtitle (b) in each rule.) For this reason, Chapters and synonymous with Subjects, and Rules are synonymous with Grades in this project. 

We will be grabbing the TEKS statements from each Chapter and Rule associated with grades 4 through 8. The [TEKSChaptersRules.csv](https://github.com/martinmarroyo/teks_pos_analysis/blob/main/TEKSChaptersRules.csv) contains a breakdown of the Chapters and Rules that will need to be extracted by the scraper. 

### Description of code and programming libraries used

The primary libraries used in this project are Pandas, BeautifulSoup, and Spacy. Pandas is used for structuring our data and writing to storage as CSV files. BeautifulSoup is used for the scraping and text extraction from the TEKS website. Spacy is used for conducting the sentiment analysis on the TEKS statements.

There are four files that all work together to perform the extraction and analysis: 
- [TEKSextraction](https://github.com/martinmarroyo/teks_pos_analysis/blob/main/src/utils/TEKSextraction.py) handles the work of scraping and extracting the text data from the website. 
- [TEKStransform](https://github.com/martinmarroyo/teks_pos_analysis/blob/main/src/utils/TEKStransform.py) does the work of transforming the extracted data as required. It transforms individual lines from TEKS into their full statements, and a collection of statements into a full TEKS chapter(subject) and rule(grade).
- [TEKSanalyze](https://github.com/martinmarroyo/teks_pos_analysis/blob/main/src/utils/TEKSanalyze.py) is responsible for the extraction and analysis of verbs from the TEKS statements.
- [main](https://github.com/martinmarroyo/teks_pos_analysis/blob/main/src/main.py) drives the program. This is where all of the functionality in the other scripts are used to actually run the extraction, transformation, and loading (ETL) of the data from TEKS. 

The model that is used with Spacy to parse our skill verbs is `en_core_web_sm`. The documenation for that can be [found here](https://spacy.io/models/en#en_core_web_sm).

### Outcome, Deliverables, and Impact

Overall, the project was a success. I was able to create a visual tool using Tableau with the data that was extracted which Celebrate Dyslexia were able to use to help create their curriculum. Because of this, the organization was able to save $7,888 which could be used for other essential needs.

- [Click here to see the final deliverable](https://public.tableau.com/shared/S6FHZFYXS?:display_count=n&:origin=viz_share_link)
- [Click here to read more about my impact on the organization through this project](https://www.catchafire.org/impact/match/2824664/celebrate-dyslexia--survey-results-analysis/)