import pandas as pd
import ast


def convert_list_to_underscore(names_list):
    if isinstance(names_list, str):  # Convert string to list if necessary
        names_list = ast.literal_eval(names_list)
        # print(names_list)
    return [name.replace(" ", "_") for name in names_list]

def convert_name_to_underscore(name):
    # if isinstance(names_list, str):  # Convert string to list if necessary
    #     names_list = ast.literal_eval(names_list)
    #     # print(names_list)
    return name.replace(" ", "_")

df = pd.read_csv('dblp.csv')
orcid_df = pd.read_csv('orcid_name_id.csv')

yearrange = list(range(2020, 2026, 1))
new_df = df[df['year'].isin(yearrange)]
new_df = new_df.groupby('booktitle')['authors_name'].apply(list)
new_df['authors_uniqie_name'] = ''
for index, row in new_df.iterrows():
    full = new_df['authors_name'][index]
    b = []
    for sublist in full:
        for item in sublist:
            b.append(item)
    new_df['authors_uniqie_name'][index] = b


new_df['unique_length_names'] = new_df['authors_uniqie_name'].apply(len)
new_df = new_df.sort_values(by = 'unique_length_names',ascending=False)


orcid_df['authors_name'] = orcid_df['authors_name'].apply(convert_name_to_underscore)
new_df['unique_orcid'] = new_df['authors_uniqie_name'].apply(lambda namelist: orcid_df[orcid_df['authors_name'].isin(namelist)]['authors_name'].nunique())

new_df['percentage_orcid'] = (new_df['unique_orcid'] * 100) / new_df['unique_length_names']
new_df = new_df.sort_values(by = 'unique_length_names',ascending=False)