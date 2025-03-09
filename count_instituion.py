# This is a sample Python script.
import pandas as pd
import networkx as nx
import numpy as np
import argparse
import os

def function(directory):
    if not os.path.exists(directory):
        return None

    filelist = os.listdir(directory)
    for file in filelist:
        print(file)
        file = os.path.join(os.getcwd(),directory,file)
        df = pd.read_csv(file)
        # df[df['Institution'].notna()]
        # Filter rows where 'Institution' is not NaN
        filtered_df = df[df['Institution'].notna()]

        # Define keywords for educational institutions and companies
        edu_keywords = ['university', 'college', 'institute', 'school']
        company_keywords = ['inc', 'llc', 'corp', 'company', 'ltd']

        # Count educational institutions and companies
        # filtered_df['Educational_Institutions'] = filtered_df[filtered_df['Institution'].str.lower().str.contains('|'.join(edu_keywords))]
        # filtered_df['Companies'] = filtered_df[filtered_df['Institution'].str.lower().str.contains('|'.join(company_keywords))]
        edu_count = filtered_df[filtered_df['Institution'].str.lower().str.contains('|'.join(edu_keywords))].shape[0]
        company_count = filtered_df[filtered_df['Institution'].str.lower().str.contains('|'.join(company_keywords))].shape[0]

        # print(filtered_df['Educational_Institutions'])
        print("Educational Institutions:", edu_count * 100 / (edu_count + company_count))
        print("Companies:", company_count * 100 / (edu_count + company_count))

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--dir",type = str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.dir)
    function(inputs.dir)