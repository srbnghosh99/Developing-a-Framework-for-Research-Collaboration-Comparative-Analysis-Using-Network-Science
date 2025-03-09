# This is a sample Python script.
import pandas as pd
import networkx as nx
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt


def function(directory):
    if not os.path.exists(directory):
        print("No existing directory")

    filelist = os.listdir(directory)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Distribution of Educational Instituion vs Company')
    for i, (file, ax) in enumerate(zip(filelist, axes.flatten())):
    # for file in filelist:
        print(file)

        filename = os.path.join(os.getcwd(),directory,file)
        df = pd.read_csv(filename)
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
        categories = ['Educational Institutions', 'Companies']
        values1 = [edu_count * 100 / (edu_count + company_count), company_count * 100 / (edu_count + company_count)]

        ax.bar(categories, values1, color='skyblue')
        for i, v in enumerate(values1): ax.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=10)
        ax.set_ylabel('Percentage')
        ax.set_title(file)

    plt.tight_layout()
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--dir",type = str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.dir)
    function(inputs.dir)
