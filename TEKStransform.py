import TEKSextraction
import os
import json
import pandas as pd


"""
    Transforms the TEKS statement pieces extracted from the website back into the full statement.
    Each statement is numbered, and everything else that follows is either marked by a letter
    or Roman Numeral.
"""
def transform(statement_pieces):
    knowledge_transform = []
    for line in statement_pieces:
        #Get first line
        if line[1].isnumeric():
            knowledge_transform.append(line)
        #Add non-numbered lines to their appropriate number
        else:
            knowledge_transform[len(knowledge_transform)-1] += (' ' + line)

    return knowledge_transform


"""
    Transforms individual statements into a full chapter and rule block of text. 
    This is used for overall analysis of word count for each verb in the
    entirety of a grade and subject.
"""
def transform_to_page(statements):
    return " ".join(statements)


"""
    Transforms collection of individual TEKS data files into a master list
"""
def write_to_master(path):
    first_file_name = os.listdir(path)[0]
    master_df = pd.read_csv(path+first_file_name)
    for file in os.listdir(path):
        if file != first_file_name:
            #create a new data frame from the file
            temp_df = pd.read_csv(path+file)
            #merge it to the master
            master_df = pd.concat([master_df,temp_df])
    master_df.to_csv(path + "master.csv")