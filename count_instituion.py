# This is a sample Python script.
import pandas as pd
import networkx as nx
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

def find_first_bracket(text):
    for i, char in enumerate(text):
        if char in "(":
            return text[:i]
    return "N/A"

def extract_latest_info(affiliation):
    if pd.isna(affiliation) or not isinstance(affiliation, str):
        return np.nan  # Return NaN if the value is missing

    # entries = affiliation.split(', ')  # Split by comma if multiple entries exist
    entries = affiliation.split("),")
    # If there's only one entry, return it as-is
    # if len(entries) == 1:
    return entries[0]

def Plot_count_institution(directory):
    # Extract institution informaiton
    if not os.path.exists(directory):
        return None
    df = pd.read_csv('/Users/shrabanighosh/PycharmProjects/orcid_extract/orcid_data_output_2.csv')
    df['Latest_Info'] = df['Employement'].apply(extract_latest_info)
    df['institution'] = df['Latest_Info'].fillna('N/A').apply(find_first_bracket)
    df = df.drop_duplicates(subset=['orcid'])
    df[['orcid', 'Name','authors_name','Researcher_URL', 'Email', 'Employement', 'institution']].to_csv('Employement.csv')

    test = df
    # test = test.rename(columns={'ID': 'orcid'})
    orcid_data = test[['orcid','Latest_Info', 'institution']]
    # fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    # fig.suptitle('Distribution of Educational Instituion vs Company')

    filelist = os.listdir(directory)
    for file in filelist:
    # for i, (file, ax) in enumerate(zip(filelist, axes.flatten())):

        filename = os.path.join(os.getcwd(), directory, file)
        sw = pd.read_csv(filename)
        sw = sw[['orcid', 'authors_name', 'Name', 'Email', 'Researcher_URL', 'Education', 'Employement', 'Qualifications']]
        merge_df = sw.merge(orcid_data, on='orcid', how='left')
        merge_df['Name'] = merge_df['Name'].fillna("")
        merge_df['Name'] = merge_df['Name'].apply(lambda x: x.replace(' ', '_'))
        # merge_df[merge_df['Institution'].notna()]
        merge_df = merge_df[
            ['orcid', 'authors_name', 'Name', 'Email', 'Researcher_URL', 'Education', 'Employement', 'Qualifications',
             'institution']]
        merge_df = merge_df.drop_duplicates(subset=['orcid'])
        merge_df = merge_df.sort_values(by=['institution'])
        print(merge_df['institution'].value_counts())
        merge_df = merge_df[merge_df['institution'] != "N/A"]
        merge_df['institution'].value_counts().nlargest(30).plot(kind='bar', figsize=(10, 5), color='skyblue')
        plt.xlabel('Institution', labelpad=25)
        plt.ylabel('Count')
        domain = file.replace(".csv", "")
        domain = domain.replace('_', ' ')
        plt.title(domain + ' Top Affiliated Institutions by Count')
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.4)  # Adjust the bottom margin to make space for xticks
        plt.savefig(domain + '.png', bbox_inches='tight',dpi='figure')
        merge_df.to_csv(filename, index=False)
        # plt.show()

        # ax.bar(merge_df['institution'].value_counts().nlargest(10).index,
        #        merge_df['institution'].value_counts().nlargest(10).values, color='skyblue')
        # ax.set_xlabel('Institution')
        # ax.set_ylabel('Count')
        # ax.set_title('Top 10 Institutions by Count')
        # ax.tick_params(axis='x', rotation=45)

        # merge_df['institution'].value_counts().nlargest(30).plot(kind='bar', figsize=(10, 5), color='skyblue')
        # # ax.set_ylabel('Percentage')
        # # ax.set_title(file)
        # ax.set_xlabel('Institution')
        # ax.set_ylabel('Count')
        # ax.set_title('Top 10 Institutions by Count')
        # ax.set_xticks(rotation=45)
        # ax.show()
    # plt.tight_layout()
    #     plt.show()

def Plot_categories(directory):
    # create visualization graph
    if not os.path.exists(directory):
        return None

    filelist = os.listdir(directory)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Distribution of Educational Instituion vs Company')
    for i, (file, ax) in enumerate(zip(filelist, axes.flatten())):
        print(file)

        filename = os.path.join(os.getcwd(),directory,file)
        df = pd.read_csv(filename)
        # df[df['Institution'].notna()]
        # Filter rows where 'Institution' is not NaN
        filtered_df = df[df['institution'].notna()]

        classified_df = pd.read_csv("classified_institutions.csv")

        merge = filtered_df.merge(classified_df, on = 'institution', how = 'inner')
        # print(merge)
        # Define keywords for educational institutions and companies
        edu_keywords = ['university']
        company_keywords = ['company']
        rc_keywords = ['research']
        merge['Category'] = np.where(merge['Category'].str.lower().str.contains('|'.join(edu_keywords)),
                                       'University', merge['Category'])
        merge['Category'] = np.where(merge['Category'].str.lower().str.contains('|'.join(company_keywords)),
                                 'Company', merge['Category'])
        merge['Category'] = np.where(merge['Category'].str.lower().str.contains('|'.join(rc_keywords)),
                                 'Research Center', merge['Category'])
        merge['Category'] = np.where(~merge['Category'].isin(['Research Center', 'Company', 'University']), 'Other', merge['Category'])
        company_count = filtered_df[filtered_df['institution'].str.lower().str.contains('|'.join(company_keywords))].shape[0]
        rc_count = filtered_df[filtered_df['institution'].str.lower().str.contains('|'.join(rc_keywords))].shape[0]

        print(merge['Category'].value_counts())
        value_count = merge['Category'].value_counts()

        ax.bar(value_count.index, value_count.values, color='skyblue')
        [ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height() / sum(value_count) * 100:.1f}%',
             ha='center', va='bottom') for bar in ax.containers[0]]
        ax.set_ylabel('Percentage')
        domain = file.replace(".csv", "")
        domain = domain.replace('_', ' ')
        ax.set_title(domain)
    plt.tight_layout()
    plt.savefig('percentage.png', bbox_inches='tight', dpi='figure')

    # plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--dir",type = str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.dir)
    Plot_count_institution(inputs.dir)
    Plot_categories(inputs.dir)
