import TEKSextraction
import os
import json
import pandas as pd

def transform(statement_pieces):
    """
    Transforms the TEKS statement pieces extracted from the website back into the full statement.
    Each statement is numbered, and everything else that follows is either marked by a letter
    or Roman Numeral.
    """
    knowledge_transform = []
    for line in statement_pieces:
        #Get first line
        if line[1].isnumeric():
            knowledge_transform.append(line)
        #Add non-numbered lines to their appropriate number
        else:
            knowledge_transform[len(knowledge_transform)-1] += (' ' + line)

    return knowledge_transform


def transform_to_page(statements):
    """
    Transforms individual statements into a full chapter and rule block of text. 
    This is used for overall analysis of word count for each verb in the
    entirety of a grade and subject.
    """
    return " ".join(statements)


def write_to_master(path):
    """
    Transforms collection of individual TEKS data files into a master list
    """
    first_file_name = os.listdir(path)[0]
    master_df = pd.read_csv(f"{path}/{first_file_name}")
    for file in os.listdir(path):
        if file != first_file_name:
            #create a new data frame from the file
            temp_df = pd.read_csv(f"{path}/{file}")
            #merge it to the master
            master_df = pd.concat([master_df,temp_df])
    master_df.to_csv(f"{path}/master.csv")
