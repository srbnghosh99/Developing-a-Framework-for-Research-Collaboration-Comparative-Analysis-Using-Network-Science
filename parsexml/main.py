import subprocess
import pandas as pd
import ast
import os
import sys

df = pd.read_csv('data/orcid_dict_new.csv')
df['ORCID_IDs'] = df['ORCID_IDs'].apply(ast.literal_eval)

for index,row in df.iterrows():
    root = '/mnt/large_data/ORCID/ORCID_2024_10_summaries/'
    folder_name = row['Last_3_Digits']
    name_info = []
    url_links = []
    affiliation_info = []
    education_info = []
    qualification_info = []
    email_info = []
    filename_list = row['ORCID_IDs']

    for file in filename_list:
        #path = folder_name + '/' + file + '.xml'
        path = os.path.join(root, folder_name, file + '.xml')
        #print(path)
        #path = root + path
        print(path)
        # Run parsexml.py with the file path as an argument
        subprocess.run([sys.executable, 'parsexml_orcid.py', '--filepath', path])