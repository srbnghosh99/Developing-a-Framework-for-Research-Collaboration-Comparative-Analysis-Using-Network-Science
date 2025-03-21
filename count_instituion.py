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
    print(filelist)
    for file in filelist:
    # for i, (file, ax) in enumerate(zip(filelist, axes.flatten())):
        if file == '.DS_Store':
            continue
        filename = os.path.join(os.getcwd(), directory, file)

        sw = pd.read_csv(filename)
        print(filename)
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
        merge_df['institution'].value_counts().nlargest(30).to_csv(file +'_top.csv')
        # merge_df['institution'].value_counts().nlargest(30).plot(kind='barh', figsize=(10, 5), color='skyblue')

        # plt.barh(institution_names, counts)  # Use barh for horizontal bars
        # plt.xlabel('Count')
        # plt.ylabel('Institution', labelpad=25)
        # domain = file.replace(".csv", "").replace('_', ' ')
        # plt.title(domain + ' Top Affiliated Institutions by Count')
        # plt.gca().invert_yaxis()  # Invert y-axis to have the highest count at the top
        # plt.subplots_adjust(left=0.4)  # Adjust left margin to fit institution names
        # plt.savefig(domain + '.png', bbox_inches='tight', dpi='figure')



        # plt.xlabel('Institution', labelpad=25)
        # plt.ylabel('Count')
        # domain = file.replace(".csv", "")
        # domain = domain.replace('_', ' ')
        # plt.title(domain + ' Top Affiliated Institutions by Count')
        # plt.xticks(rotation=90)
        # plt.subplots_adjust(bottom=0.4)  # Adjust the bottom margin to make space for xticks
        # plt.savefig(domain + '.png', bbox_inches='tight', dpi='figure')
        # merge_df.to_csv(filename, index=False)

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
    # df.set_index("institution", inplace=True)  # Set 'institution' as index for easier replacement
    # df.loc[df2["institution"], "category"] = df2.set_index("institution")["category"]
    # df.reset_index(inplace=True)  # Reset index if needed


    # create visualization graph
    if not os.path.exists(directory):
        return None

    filelist = os.listdir(directory)
    print(filelist)
    filelist.remove('.DS_Store')
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Distribution of Institution Categories')
    for i, (file, ax) in enumerate(zip(filelist, axes.flatten())):
        print(file)

        filename = os.path.join(os.getcwd(),directory,file)
        df = pd.read_csv(filename)
        filtered_df = df[df['institution'].notna()]
        classified_df = pd.read_csv("classified_institutions3.csv")
        edu_keywords = ['university']
        company_keywords = ['Inc.']
        rc_keywords = ['research center','research institute']
        rcl_keywords = ['lab','company research']
        # classified_df['Category'] = classified_df.loc[classified_df['Category'].str.lower().str.contains('university'),'University']
        classified_df.loc[classified_df['Category'].str.lower().str.contains('|'.join(edu_keywords),na=False), 'Category'] = 'Company Research Lab'
        classified_df.loc[classified_df['Category'].str.lower().str.contains('|'.join(rcl_keywords), na=False), 'Category'] = 'Company Research Lab'
        classified_df.loc[classified_df['Category'].str.lower().str.contains('|'.join(rc_keywords), na=False), 'Category'] = 'Research Center'
        classified_df.loc[classified_df['Category'].str.lower().str.contains('|'.join(company_keywords), na=False), 'Category'] = 'Company'
        classified_df.loc[~classified_df['Category'].isin(['Research Center', 'Company', 'University', 'Company Research Lab']), 'Category'] = 'Other'

        print(classified_df['Category'].value_counts())
        classified_df = pd.read_csv("classified_institutions4.csv")
        print(filtered_df.columns)
        filtered_df = filtered_df[['orcid', 'authors_name',
        'Name', 'Email', 'Researcher_URL', 'Education', 'Employement',
        'Qualifications', 'institution']]

        merge = filtered_df.merge(classified_df, on='institution', how='inner')
        print(merge['Category'].value_counts())
        value_count = merge['Category'].value_counts()

        ax.bar(value_count.index, value_count.values, color='skyblue')
        [ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height() / sum(value_count) * 100:.1f}%',
             ha='center', va='bottom') for bar in ax.containers[0]]
        ax.set_ylabel('Percentage')
        domain = file.replace(".csv", "")
        domain = domain.replace('_', ' ')
        ax.set_title(domain); ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('percentage.png', bbox_inches='tight', dpi='figure')

    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--dir",type = str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.dir)
    # Plot_count_institution(inputs.dir)
    Plot_categories(inputs.dir)

    # classified_df['Category'] = np.where(classified_df['Category'].str.lower().str.contains('|'.join(edu_keywords)),
    #                                      'University', classified_df['Category'])