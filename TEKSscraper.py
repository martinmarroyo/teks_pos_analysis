import TEKSextraction as te
import pandas as pd
import time
import json

# TEKS Chapters and Rules contains the necessary pointers to the rule and chapter that we need. 
# It also has the grade levels and subject that we want to work on.
f = open('directories.json',)
paths = json.load(f)
csv_path= paths['path_to_teks_ch_rules']
teks_ch_rules = pd.read_csv(csv_path)


"""
Loading the TEKS chapters and rules and iterating over it to extract the data

The general idea is to:

-Load in our TEKS Chapters and Rules CSV
-For each line in the CSV, we will take the chapter and rule and pass it to our extraction function
-After the extraction happens, a new csv will be created from the extracted data. It will be named in the following structure: {Subject}-{Grade Level}
-Each line from the extracted text will be put into the new CSV as a single column
-Then the CSV will be written back to the TEKS folder
"""

for index,row in teks_ch_rules.iterrows():
    # Extract row information
    subject = row['Subject']
    grade = row['Grade Level Indicated']
    chapter = row['Chapter']
    rule = row['Rule']
    # Create DataFrame by extracting TEKS data
    teks_dir = paths['path_to_teks_dir']
    csv_name = f"{subject}-{grade}.csv"
    df = pd.DataFrame(te.extract_teks(chapter,rule), columns=['Statements'])
    # Write the DataFrame to our folder as a CSV
    df.to_csv(teks_dir + csv_name)
    # Create a 10 second delay to avoid multiple server calls back-to-back
    time.sleep(10)