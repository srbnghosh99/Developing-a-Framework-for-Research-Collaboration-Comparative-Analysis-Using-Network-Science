import os
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parsexml(file_path):
    # Define file path
    # file_path = "0000-0001-9918-3000.xml"

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Oops! The file '{file_path}' was not found. Please check the filename and try again. 😊")
        exit()
    elif os.path.getsize(file_path) == 0:
        print(f"The file '{file_path}' is empty. Please provide a valid XML file. 📂")
        exit()
    else:
        # Load XML file
        print(f"The file '{file_path}' found. 📂")
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define namespaces
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

        # Extract and print email if found
        email = email_element.text if email_element is not None else "N/A"
        

        # Extract researcher URLs
        researcher_urls = [url.text for url in root.findall(".//researcher-url:researcher-url/common:url", ns)]
        researcher_urls_name = root.find(".//researcher-url:url-name",ns)
        researcher_urls_link = root.find(".//researcher-url:url",ns)
        researcher_urls = f"{researcher_urls_name.text}: {researcher_urls_link.text}" if researcher_urls_name is not None and researcher_urls_link is not None else "N/A"


        # Extract educational affiliations
        education_list = []
        for edu in root.findall(".//education:education-summary", ns):
            institution = edu.find(".//common:organization/common:name", ns)
            role = edu.find(".//common:role-title", ns)
            if institution is not None:
                education_list.append({
                    "Institution": institution.text,
                    "Role": role.text if role is not None else "N/A",
                    "Type": "Education"
                })

        # Extract employment affiliations
        employment_list = []
        for emp in root.findall(".//employment:employment-summary", ns):
            institution = emp.find(".//common:organization/common:name", ns)
            role = emp.find(".//common:role-title", ns)
            if institution is not None:
                employment_list.append({
                    "Institution": institution.text,
                    "Role": role.text if role is not None else "N/A",
                    "Type": "Employment"
                })

        # Combine results
        affiliations = education_list + employment_list

        qualification_list = []
        for qual in root.findall(".//qualification:qualification-summary", ns):
            institution = qual.find(".//common:organization/common:name", ns)
            role = qual.find(".//common:role-title", ns)
            if institution is not None:
                qualification_list.append(f"{institution.text} ({role.text if role is not None else 'N/A'})")


        # # Display results
        # print(f"Full Name: {full_name}\n")
        # print("\Email:")
        # print("\n".join(email) if email else "No email found.")

        print(f"Name: {full_name}")
        if affiliations:
            print("Affiliations:")
            for aff in affiliations:
                print(f"- {aff['Institution']} ({aff['Role']} - {aff['Type']})")

        # if qualification_list:
        #     print("qualification:")
        #     for qual in qualification_list:
        #         print(f"- {qual['Institution']} ({qual['Role']} - {qual['Type']})")

        # print("Education:")
        # print("\n".join(education_list) if education_list else "No education details found.")

        print("\nQualifications:")
        print("\n".join(qualification_list) if qualification_list else "No qualification details found.")

        print("\nResearcher URLs:")
        print(researcher_urls)

        
        print(f"Email: {email}")
        # print("\n".join(researcher_urls) if researcher_urls else "No researcher URLs found.")


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--filepath",type = str)
    # parser.add_argument("--outputfilename",type = str)
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.filepath)
    # print(inputs.outputfilename)
    parsexml(inputs.filepath)


    

