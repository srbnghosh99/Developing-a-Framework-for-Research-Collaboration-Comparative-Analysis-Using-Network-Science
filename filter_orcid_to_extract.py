import pandas as pd
import ast
from collections import defaultdict

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

df = pd.read_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/dblp.csv')
df['authors_name'] = df['authors_name'].apply(ast.literal_eval)

conflist = ['CIKM','KDD','SIGIR','WWW','WSDM','IEEE BigData', 'ICDM', 'ASONAM', 'ICML','ICSE','ASE', 'ESEC/SIGSOFT FSE' ,'COMPSAC' , 'ISSTA' , 'UIST',
 'HRI','HRI (Companion)','ROBIO' , 'IROS' , 'ICRA','CVPR', 'ICCV' , 'ICPR' , 'WACV' ]


yearrange = list(range(2022, 2026, 1)) 
new_df = df[df['year'].isin(yearrange)]
new_df = new_df[new_df['booktitle'].isin(conflist)]
new_df.shape
masterlist = new_df['authors_name'].tolist()
flat_list = []
for sublist in masterlist:
    for item in sublist:
        flat_list.append(item)

orcid = pd.read_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/final_files/unique_orcids.csv')
filtered_orcid = orcid[orcid['authors_name'].isin(flat_list)]
orcid_dict = defaultdict(list)
for orcid in filtered_orcid['orcid']:
    last_four = orcid[-3:]  # Extract last 4 digits
    orcid_dict[last_four].append(orcid)  # Group by last four digits



df_dict = pd.DataFrame([(k, ', '.join(v)) for k, v in orcid_dict.items()], columns=['Last_3_Digits', 'ORCID_IDs'])
# print(df_dict)
df_dict = df_dict.sort_values(by='Last_3_Digits')
df_dict.to_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/latest_files/orcid_dict_new.csv', index=False)

# # Load back from CSV
df_loaded = pd.read_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/latest_files/orcid_dict_new.csv')

print(df_loaded)