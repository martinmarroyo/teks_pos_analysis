import TEKSextraction as te
import TEKStransform as tf
import TEKSanalyze as ta
import pandas as pd
import time
import json


"""
Loading the TEKS chapters and rules and iterating over it to extract the data

The general idea is to:

-Load in our TEKS Chapters and Rules CSV
-For each line in the CSV, we will take the chapter and rule and pass it to our extraction function
-After the extraction happens, a new csv will be created from the extracted data. It will be named in the following structure: {Subject}-{Grade Level}
-Each line from the extracted text will be transformed into its original structure (meaning each statement will be numbered and will include all substatements)
-Each statement will have a list of identified Verb/Skills associated with it in a separate column as well as the associated grade and subject 
-Then the CSV will be written back to the TEKS statements folder
-Additionally, the individual TEKS statements will be transformed into a whole page (the entire set of statements for a chapter(subject) and rule(grade))
-These full statements will be analyzed and the verbs associated with these statements will be counted and put into an analysis file
-The analysis file names will follow this structure: {Subject}-{Grade}_verb_frequency
-After all of the individual files have been written, master files will be created that are a union of all the tables/files for the statements and analysis sets
"""


if __name__ == '__main__':
    
    # TEKS Chapters and Rules contains the necessary pointers to the rule and chapter that we need. 
    # It also has the grade levels and subject that we want to work on.
    f = open('directories.json',)
    paths = json.load(f)
    csv_path= paths['path_to_teks_ch_rules']
    teks_ch_rules = pd.read_csv(csv_path)
    
    for index,row in teks_ch_rules.iterrows():
        # Extract row information
        subject = row['Subject']
        grade = row['Grade Level Indicated']
        chapter = row['Chapter']
        rule = row['Rule']
        # Create DataFrame by extracting TEKS data
        teks_dir = paths['path_to_teks_dir']
        csv_name = f"{subject}-{grade}.csv"
        teks_statements = tf.transform(te.extract_teks(chapter,rule))
        teks_statement_verbs = ta.get_verbs(teks_statements)
        teks_statements_table = pd.DataFrame({'Statement':teks_statements, 'Verbs/Skills':teks_statement_verbs,'Grade': grade,'Subject':subject})
        # Write the DataFrame to our folder as a CSV
        teks_statements_table.to_csv(teks_dir + csv_name)
        # Create analysis tables for each TEKS page
        # Transform collection of statements into a full page
        teks_page_verbs = ta.get_verbs(tf.transform_to_page(teks_statements), whole_page=True)
        # Get the verbs and frequencies of each
        verb,frequency = ta.get_verbs_and_counts(teks_page_verbs)
        teks_analysis_table = pd.DataFrame({'Verb/Skill':verb,'Frequency':frequency,'Grade': grade,'Subject':subject})
        # Naming for the analysis tables
        csv_analysis_name = f"{subject}-{grade}_verb_frequency.csv"
        # Write the table to our director
        teks_analysis_table.to_csv(paths['path_to_teks_analysis']+csv_analysis_name)
        # Create a 10 second delay to avoid multiple server calls back-to-back
        time.sleep(10)


    """
        After all of our data is extracted into individual files and folders,
        create master files for our statements and analysis files
    """
    # Analysis folder
    tf.write_to_master(paths["path_to_teks_analysis"])
    # Statements folder
    tf.write_to_master(paths["path_to_teks_dir"])
