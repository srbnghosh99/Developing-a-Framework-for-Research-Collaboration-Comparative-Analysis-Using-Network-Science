import os
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys
import ast


def readfile(inputfile):
    """ Reads input file and processes ORCID XML data. """

    df = pd.read_csv(inputfile)
    df['ORCID_IDs'] = df['ORCID_IDs'].apply(ast.literal_eval)

    # Master lists to store extracted data
    master_names = []
    master_affiliations = []
    master_qualifications = []
    master_researcher_urls = []
    master_emails = []

    root_dir = '/mnt/large_data/ORCID_2024_10_summaries/'

    for _, row in df.iterrows():
        folder_name = row['Last_3_Digits']
        orcid_files = row['ORCID_IDs']

        for file in orcid_files:
            path = os.path.join(root_dir, folder_name, file + '.xml')
            name, email, researcher_url, affiliations, qualifications = parsexml(path)

            # Append to master lists
            master_names.append(name)
            master_emails.append(email)
            master_researcher_urls.append(researcher_url)
            master_affiliations.append(", ".join(affiliations) if affiliations else "N/A")
            master_qualifications.append(", ".join(qualifications) if qualifications else "N/A")

    # Create DataFrame
    df_output = pd.DataFrame({
        "Name": master_names,
        "Email": master_emails,
        "Researcher_URL": master_researcher_urls,
        "Affiliations": master_affiliations,
        "Qualifications": master_qualifications
    })

    # Save to CSV (optional)
    output_path = "orcid_data_output.csv"
    df_output.to_csv(output_path, index=False)
    
    print(f"\n✅ Data processing complete. Results saved to {output_path}")
    print(df_output.head())  # Display first few rows


def parsexml(file_path):
    """ Parses XML file and extracts researcher details. """

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"⚠️ Skipping {file_path} (File missing or empty)")
        return "N/A", "N/A", "N/A", [], []

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

    # Extract educational & employment affiliations
    affiliations = []
    for section, section_type in [("education:education-summary", "Education"), ("employment:employment-summary", "Employment")]:
        for entry in root.findall(f".//{section}", ns):
            institution = entry.find(".//common:organization/common:name", ns)
            role = entry.find(".//common:role-title", ns)
            if institution is not None:
                affiliations.append(f"{institution.text} ({role.text if role is not None else 'N/A'}) - {section_type}")

    # Extract qualifications
    qualifications = []
    for qual in root.findall(".//qualification:qualification-summary", ns):
        institution = qual.find(".//common:organization/common:name", ns)
        role = qual.find(".//common:role-title", ns)
        if institution is not None:
            qualifications.append(f"{institution.text} ({role.text if role is not None else 'N/A'})")

    return full_name, email, researcher_url, affiliations, qualifications


def parse_args():
    parser = argparse.ArgumentParser(description="Process ORCID XML Files")
    parser.add_argument("--filepath", type=str, required=True, help="Path to input CSV file")
    return parser.parse_args()


if __name__ == '__main__':
    inputs = parse_args()
    print(f"📂 Processing ORCID data from: {inputs.filepath}")
    readfile(inputs.filepath)
