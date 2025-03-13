import pandas as pd
import ast
SW = ['ICSE','ASE', 'ESEC/SIGSOFT FSE' ,'COMPSAC' , 'ISSTA' , 'UIST' ]
DM = ['CIKM','KDD','SIGIR','WWW','WSDM','IEEE BigData']
HRI=['HRI','HRI (Companion)','ROBIO' , 'IROS' , 'ICRA']
CV = ['CVPR', 'CVPR Workshops' , 'ICCV' , 'ICPR' , 'WACV' ]


# conflist = ['CIKM','KDD','SIGIR','WWW','WSDM','IEEE BigData','ICSE','ASE', 'ESEC/SIGSOFT FSE' ,'COMPSAC' , 'ISSTA' , 'UIST',
#  'HRI','HRI (Companion)','ROBIO' , 'IROS' , 'ICRA','CVPR', 'ICCV' , 'ICPR' , 'WACV' ]
def function():
    conflist = [SW,DM,HRI,CV]
    df = pd.read_csv('final_files/selected_confs_orcid_2022_2024.csv')
    df = df[['booktitle','authors_uniqie_name','percentage_orcid']]
    df_orcid = pd.read_csv("final_files/extract_orcids.csv")
    orcid_data = pd.read_csv('orcid_data_output_2.csv')
    orcid_data = orcid_data.rename(columns={'ID': 'orcid'})
    for domain in conflist:
        df_new = df[df['booktitle'].isin(domain)]
        # df_sw = df[df['booktitle'].isin(swlist)]
        df_new['authors_uniqie_name'] = df_new['authors_uniqie_name'].apply(ast.literal_eval)
        dfs = []
        for index, row in df_new.iterrows():
          namelist = row['authors_uniqie_name']
          processed_names = [name.replace('_', ' ') for name in namelist]
          dfs.append(df_orcid[df_orcid['authors_name'].isin(processed_names)])
        final_df = pd.concat(dfs, ignore_index=True)
        merge_df = final_df.merge(orcid_data, on = 'orcid', how = 'left')
        filename =[var_name for var_name in globals() if globals()[var_name] is domain][0]
        filename = filename + '.csv'
        merge_df.to_csv(filename)

if __name__ == '__main__':
    function()