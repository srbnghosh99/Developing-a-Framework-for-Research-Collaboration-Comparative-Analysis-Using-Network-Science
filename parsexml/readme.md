# README

## Overview
This document provides details on the input and output files for the following scripts:
1. `parsedblp.py`
2. `parseorcid.py`

## 1. parsedblp.py

### **Input File**
- **Format**: CSV
- **Expected Columns**:
  - `Column1`: Description
  - `Column2`: Description
  - ...

### **Output File**
- **Format**: CSV / JSON / TXT (Specify)
- **Contents**:
  - Processed data from the input file.
  - Additional extracted or transformed information.

## 2. parseorcid.py

### **Input File**
- **Format**: CSV containing ORCID IDs
- **Expected Columns**:
  - `ORCID_IDs`: A list of ORCID identifiers.
  - `Last_3_Digits`: A folder name identifier.

### **Output Files**
- **Format**: CSV / JSON / TXT (Specify)
- **Contents**:
  - Extracted researcher details (name, email, affiliations, etc.).
  - Aggregated data on research profiles.

## Usage
Run the scripts using the following command:
```bash
python parsedblp.py --input input_file.csv --output output_file.csv
python parseorcid.py --filepath input_file.csv
