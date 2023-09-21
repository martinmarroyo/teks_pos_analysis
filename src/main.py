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
import utils.TEKSextraction as te
import utils.TEKStransform as tf
import utils.TEKSanalyze as ta
import pandas as pd
import time
import json
import spacy
import sys
import subprocess
from yaml import load, SafeLoader
from loguru import logger
from tqdm import tqdm
from pathlib import Path

def main(nlp, paths, teks_ch_rules, base_url):
    for index, row in tqdm(teks_ch_rules.iterrows(), total=teks_ch_rules.shape[0]):
        # Extract row information
        subject = row['Subject']
        grade = row['Grade Level Indicated']
        chapter = row['Chapter']
        rule = row['Rule']
        # Create DataFrame by extracting TEKS data
        teks_dir = paths['teks_output_dir']
        csv_name = f"{subject}-{grade}.csv"
        teks_statements = tf.transform(te.extract_teks(base_url, chapter, rule))
        teks_statement_verbs = ta.get_verbs(nlp, teks_statements)
        teks_statements_table = pd.DataFrame({'Statement':teks_statements, 'Verbs/Skills':teks_statement_verbs,'Grade': grade,'Subject':subject})
        # Write the DataFrame to our folder as a CSV
        teks_statements_table.to_csv(f"{teks_dir}/{csv_name}")
        # Create analysis tables for each TEKS page
        # Transform collection of statements into a full page
        teks_page_verbs = ta.get_verbs(nlp, tf.transform_to_page(teks_statements), whole_page=True)
        # Get the verbs and frequencies of each
        verb,frequency = ta.get_verbs_and_counts(teks_page_verbs)
        teks_analysis_table = pd.DataFrame({'Verb/Skill':verb,'Frequency':frequency,'Grade': grade,'Subject':subject})
        # Naming for the analysis tables
        csv_analysis_name = f"{subject}-{grade}_verb_frequency.csv"
        # Write the table to our directory
        # teks_analysis_output_dir
        teks_analysis_table.to_csv(f"{paths['teks_analysis_output_dir']}/{csv_analysis_name}")
        # Create a delay to avoid multiple server calls back-to-back
        time.sleep(paths["delay_seconds"])
    # After all of our data is extracted into individual files and folders,
    # create master files for our statements and analysis files
    # Analysis folder
    logger.info("Writing data to storage...")
    print(paths["teks_analysis_output_dir"])
    tf.write_to_master(paths["teks_analysis_output_dir"])
    # Statements folder
    tf.write_to_master(paths["teks_output_dir"])


if __name__ == '__main__': 
    # TEKS Chapters and Rules contains the necessary pointers to the rule and chapter that we need. 
    # It also has the grade levels and subject that we want to work on.
    with open("config.yaml", "r") as f:
        paths = load(f, Loader=SafeLoader)
    # Add utils module to python path
    sys.path.append(Path.cwd()/"utils")
    # Install and load the model
    logger.info("Installing the en_core_web_sm model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    logger.info("Loading the en_core_web_sm model")
    nlp = spacy.load("en_core_web_sm")
    logger.info("Loading in the TEKS Chapter Rules...")
    csv_path= paths['teks_ch_rules_dir']
    teks_ch_rules = pd.read_csv(csv_path)
    base_url = "https://texreg.sos.state.tx.us/public/"
    logger.info("Beginning to extract data from TEKS. Estimated processing time is 20 minutes...")
    main(nlp, paths, teks_ch_rules, base_url)
    logger.info("TEKS Extraction complete!")