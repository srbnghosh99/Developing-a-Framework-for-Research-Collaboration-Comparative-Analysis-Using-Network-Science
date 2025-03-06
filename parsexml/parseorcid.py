import os
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys
import ast
from tqdm import tqdm

def readfile(inputfile):
    """ Reads input file and processes ORCID XML data. """

    df = pd.read_csv(inputfile)
    print('Number of orcids',df['len'].sum())
    df['ORCID_IDs'] = df['ORCID_IDs'].apply(ast.literal_eval)

    # Master lists to store extracted data
    master_id = []
    master_names = []
    master_affiliations = []
    master_education = []
    master_employement = []
    master_qualifications = []
    master_researcher_urls = []
    master_emails = []

    root_dir = '/mnt/large_data/ORCID_2024_10_summaries/'


    for _, row in df.iterrows():
        folder_name = row['Last_3_Digits']
        orcid_files = row['ORCID_IDs']

        #for file in orcid_files:
        for file in tqdm(orcid_files, desc="Processing ORCID Files"):
            path = os.path.join(root_dir, folder_name, file + '.xml')
            #print(file)
            name, email, researcher_url, education_list, employment_list, qualifications = parsexml(path)

            # Append to master lists
            master_id.append(file)
            master_names.append(name)
            master_emails.append(email)
            master_researcher_urls.append(researcher_url)            
            master_employement.append(", ".join([f"{emp.get('Institution', 'N/A')} ({emp.get('Department', 'N/A')}) ({emp.get('Role', 'N/A')} - {emp.get('Type', 'N/A')}) ({emp.get('Startdate', 'N/A')})" for emp in                   employment_list]) if employment_list else "N/A")

            master_education.append(", ".join([f"{edu.get('Institution', 'N/A')} ({edu.get('Department', 'N/A')}) ({edu.get('Role', 'N/A')} - {edu.get('Type', 'N/A')}) ({edu.get('Startdate', 'N/A')})" for edu in 
                education_list]) if education_list else "N/A")
            #master_employement.append(", ".join(employment_list) if employment_list else "N/A")
            #master_education.append(", ".join(education_list) if education_list else "N/A")
            master_qualifications.append(", ".join(qualifications) if qualifications else "N/A")

    # Create DataFrame
    df_output = pd.DataFrame({
        "ID": master_id,
        "Name": master_names,
        "Email": master_emails,
        "Researcher_URL": master_researcher_urls,
        # "Affiliations": master_affiliations,
        "Education": master_education,
        "Employement": master_employement,
        "Qualifications": master_qualifications
    })

    # Save to CSV (optional)
    output_path = "orcid_data_output_2.csv"
    df_output.to_csv(output_path, index=False)
    
    print(f"\n✅ Data processing complete. Results saved to {output_path}")
    print(df_output.head())  # Display first few rows


def parsexml(file_path):
    """ Parses XML file and extracts researcher details. """

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"⚠️ Skipping {file_path} (File missing or empty)")
        return "N/A", "N/A", "N/A", [], [], []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {
        'common': 'http://www.orcid.org/ns/common',
        'person': 'http://www.orcid.org/ns/person',
        'education': 'http://www.orcid.org/ns/education',
        'employment': 'http://www.orcid.org/ns/employment',
        'qualification': 'http://www.orcid.org/ns/qualification',
        'researcher-url': 'http://www.orcid.org/ns/researcher-url',
        'email': 'http://www.orcid.org/ns/email',
        'personal-details': 'http://www.orcid.org/ns/personal-details',
    }

    # Extract full name
    given_name = root.find(".//personal-details:given-names", ns)
    family_name = root.find(".//personal-details:family-name", ns)
    full_name = f"{given_name.text} {family_name.text}" if given_name is not None and family_name is not None else "N/A"

    # Extract email
    email_element = root.find(".//email:email/email:email", ns)
    email = email_element.text if email_element is not None else "N/A"

    # Extract researcher URL
    researcher_urls_name = root.find(".//researcher-url:url-name", ns)
    researcher_urls_link = root.find(".//researcher-url:url", ns)
    researcher_url = f"{researcher_urls_name.text}: {researcher_urls_link.text}" if researcher_urls_name is not None and researcher_urls_link is not None else "N/A"

    employment_list = []
    for emp in root.findall(".//employment:employment-summary", ns):
        institution = emp.find(".//common:organization/common:name", ns)
        role = emp.find(".//common:role-title", ns)
        department = emp.find(".//common:department-name", ns)
        startdate = emp.find(".//common:start-date/common:year", ns)
        # year = emp.find(".//common:start-date", ns)
        if institution is not None:
            employment_list.append({
                "Institution": institution.text,
                "Role": role.text if role is not None else "N/A",
                "Department": department.text if department is not None else "N/A",
                "Startdate": startdate.text if startdate is not None else "N/A",
                "Type": "Employment"
            })
    education_list = []
    for edu in root.findall(".//education:education-summary", ns):
        institution = edu.find(".//common:organization/common:name", ns)
        role = edu.find(".//common:role-title", ns)
        department = edu.find(".//common:department-name", ns)
        startdate = edu.find(".//common:start-date/common:year", ns)
        if institution is not None:
            education_list.append({
                "Institution": institution.text,
                "Role": role.text if role is not None else "N/A",
                "Department": department.text if department is not None else "N/A",
                "Startdate": startdate.text if startdate is not None else "N/A",
                "Type": "Education"
            })

    # Extract educational & employment affiliations
    # affiliations = []
    # for section, section_type in [("education:education-summary", "Education"), ("employment:employment-summary", "Employment")]:
    #     for entry in root.findall(f".//{section}", ns):
    #         institution = entry.find(".//common:organization/common:name", ns)
    #         role = entry.find(".//common:role-title", ns)
    #         if institution is not None:
    #             affiliations.append(f"{institution.text} ({role.text if role is not None else 'N/A'}) - {section_type}")

    # Extract qualifications
    qualifications = []
    for qual in root.findall(".//qualification:qualification-summary", ns):
        institution = qual.find(".//common:organization/common:name", ns)
        role = qual.find(".//common:role-title", ns)
        if institution is not None:
            qualifications.append(f"{institution.text} ({role.text if role is not None else 'N/A'})")
    '''
    if education_list:
        print("Education:")
        for aff in education_list:
            print(f"- {aff['Institution']} ({aff['Department']}) ({aff['Role']} - {aff['Type']}) ({aff['Startdate']})")

    if employment_list:
        print("Employement:")
        for qual in employment_list:
             print(f"- {qual['Institution']} ({qual['Department']}) ({qual['Role']} - {qual['Type']}) ({qual['Startdate']})")
    '''
    return full_name, email, researcher_url, education_list, employment_list, qualifications


def parse_args():
    parser = argparse.ArgumentParser(description="Process ORCID XML Files")
    parser.add_argument("--filepath", type=str, required=True, help="Path to input CSV file")
    return parser.parse_args()


if __name__ == '__main__':
    inputs = parse_args()
    print(f"📂 Processing ORCID data from: {inputs.filepath}")
    readfile(inputs.filepath)
