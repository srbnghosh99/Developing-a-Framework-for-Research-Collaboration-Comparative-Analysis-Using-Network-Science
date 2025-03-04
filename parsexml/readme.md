# README

## Overview
This document provides details on the input and output files for the following scripts:
1. `parsedblp.py`
2. `parseorcid.py`

## 1. parsedblp.py

### **Input File**
- **Format**: xml
- **Expected Columns**:
- extract mdate ,name, title, crossref, pages, year, key, ee, url, date, booktitle, orcid id.  

### **Output File**
- **Format**: CSV (Specify)
- **Contents**:
  - Processed data from the input file and return dataframe which contains columns extract mdate ,name, title, crossref, pages, year, key, ee, url, date, booktitle, orcid id. 

## 2. parseorcid.py

### **Input File**
- **Format**: CSV containing ORCID IDs
- **Expected Columns**:
  - `Last_3_Digits`: A folder name identifier (total 1100)
  - `ORCID_IDs`: A list of ORCID identifiers (under each Last_3_Digits identifier)


### **Output Files**
- **Format**: CSV / JSON / TXT (Specify)
- **Contents**:
  - Extracted researcher details (name, email, affiliations, etc.).

## Usage
Run the scripts using the following command:
```bash
python parsedblp.py --input input_file.xml --outputdirectory output/
python parseorcid.py --filepath input_file.csv
