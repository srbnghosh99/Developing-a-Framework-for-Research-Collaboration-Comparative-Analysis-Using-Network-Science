
import pandas as pd
import itertools
import ast

def convert_name_to_underscore(name):
    # if isinstance(names_list, str):  # Convert string to list if necessary
    #     names_list = ast.literal_eval(names_list)
    #     # print(names_list)
    return name.replace(" ", "_")


df = pd.read_csv("/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/orcid_percentage_2022_2024.csv")
df['authors_uniqie_name'] = df['authors_uniqie_name'].apply(ast.literal_eval)
conflist = ['CIKM','KDD','SIGIR','WWW','WSDM','IEEE BigData', 'ICDM', 'ASONAM', 'RecSys', 'ICDM Workshops', 'ICDE', 'ICMLA','ICSE','ASE', 'ESEC/SIGSOFT FSE' ,'COMPSAC' , 'ISSTA' , 'UIST','HRI','HRI (Companion)','ROBIO' , 'IROS' , 'ICRA','CVPR', 'CVPR Workshops' , 'ICCV' , 'ICPR' , 'WACV']




orcid_df = pd.read_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/orcid_name_id.csv')
orcid_df['authors_name'] = orcid_df['authors_name'].apply(convert_name_to_underscore)
authors_name_list = df['authors_uniqie_name'].tolist()
authors_names = list(itertools.chain.from_iterable(authors_name_list))

new_orcid = orcid_df[orcid_df['authors_name'].isin(authors_names)]
new_orcid.drop_duplicates(subset=['orcid'])

print(f"{(orcid_df[orcid_df['authors_name'].isin(authors_names)]['orcid'].nunique()*100)/len(set(authors_names))}%")