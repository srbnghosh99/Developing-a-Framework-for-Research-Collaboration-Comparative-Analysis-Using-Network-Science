# Developing-a-Framework-for-Research-Collaboration-Network-Analysis-Using-Network-Science

1. filter_domain_orcid.py
-after getting orcid infomation, orcids are filtered for each domain for chosen conferences.
2. create_graph.py
   - from Authors list from papers, create co-authorship graph from the list
   - ```bash
     python3 create_graph.py --inputfilename graphs_filtered_2022_2025/dblp_cv_filtered_2022_2025.csv --outputfilename graphs_filtered_2022_2025/dblp_cv_filtered_2022_2025.graphml
   
3. Count number of institutions either educational or companybased (for all domains) and show histogram
   - python3 count_instituion.py --dir domains
