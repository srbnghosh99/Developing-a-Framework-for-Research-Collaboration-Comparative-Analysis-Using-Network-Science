import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
import argparse


def collab_type(lst):
    # print(len(lst))
    lst = [cat for cat in lst if cat != 'DA']
    if(len(set(lst)) > 1):
        return 'inter_collab'
    # if all(x == lst[0] for x in lst):
    else:
        return 'intra_collab'

def get_aff_info(file1,file2):

    df_class = pd.read_csv('classified_institutions.csv')
    df = pd.read_csv(file1)
    print(df.shape)
    df = df.merge(df_class, on = 'institution', how = 'left')
    df['Category'].fillna('DA', inplace=True)
    df['institution'].fillna('DA', inplace=True)
    df.to_csv(file1)

    authors_info = pd.read_csv(file1)
    authors_info['Category'].fillna('DA', inplace=True)
    authors_info['institution'].fillna('DA', inplace=True)
    # print(authors_info['Category'].value_counts())
    # authors_info.to_csv(file1)
    # print(df), print(authors_info)



    df = pd.read_csv(file2)
    df[['authors_name', 'authors_orcid']]
    df['authors_name'] = df['authors_name'].apply(ast.literal_eval)

    df['authors_aff'] =''
    df['authors_ins'] = ''
    for index,row in df.iterrows():
        lis = row['authors_name']
        aff =authors_info[authors_info['authors_name'].isin(lis)]
        aff_mapping = aff.set_index('authors_name')['Category'].to_dict()
        aff_institution = aff.set_index('authors_name')['institution'].to_dict()
        # Generate the final list with mapped values or 'DA' if not found
        aff_list = [aff_mapping.get(name, 'DA') for name in lis]
        # ins_list = [aff_institution.get(name, 'DA') if name == name else 'DA' for name in lis]

        ins_list = [aff_institution.get(name, 'DA') for name in lis]
        df.at[index, 'authors_aff'] = aff_list
        df.at[index, 'authors_ins'] = ins_list
    df['collab_type'] = df['authors_aff'].apply(collab_type)
    print(df[['authors_aff', 'authors_ins']])
    print(df.columns)
    df = df[['authors_name','authors_orcid', 'title', 'pages', 'year', 'data', 'key', 'ee', 'url',
       'booktitle', 'crossref', 'authors_aff','authors_ins','collab_type']]
    df.to_csv(file2)


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--file1",type = str)
    parser.add_argument("--file2", type=str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    # print(inputs.dir)
    get_aff_info(inputs.file1,inputs.file2)




