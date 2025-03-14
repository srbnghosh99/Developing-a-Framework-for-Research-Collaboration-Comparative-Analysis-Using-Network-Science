#python3 parsexml_orcid.py --filepath 0000-0001-5749-3000.xml
#python3 parsexml_orcid.py --filepath 0009-0008-3019-1000.xml
#python3 parsexml_orcid.py --filepath 0000-0002-0999-4000.xml
#python3 parsexml_orcid.py --filepath 0000-0001-9918-3000.xml


#!/bin/bash


#directory="/Users/shrabanighosh/PycharmProjects/orcid_extract/graphs"  # Replace with actual path
#files=($(ls "$directory"))
#
#for ((i=0; i<${#files[@]}; i++)); do
#    for ((j=i+1; j<${#files[@]}; j++)); do
#        if [[ ${files[i]} == *.graphml && ${files[j]} == *.graphml ]]; then
#            csv_file1="${files[i]%.graphml}.csv"
#            csv_file2="${files[j]%.graphml}.csv"
#            python overlapping_nodes.py --graphfile1 "$directory/${files[i]}" --graphfile2 "$directory/${files[j]}" --file1 "$directory/${csv_file1}" --file2 "$directory/${csv_file2}"
#        fi
##        python overlapping_nodes.py --graphfile1 "$directory/${files[i]}" --graphfile2 "$directory/${files[j]}"
#    done
#done


python3 overlapping_nodes\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml --file1 graphs/dblp_cv_filtered_2022_2025.csv  --file2 graphs/dblp_hri_filtered_2022_2025.csv  --file3 graphs/dblp_dm_filtered_2022_2025.csv

python3 create_bipartite\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml -outfile tripart1.graphml

python3 overlapping_nodes\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_sw_filtered_2022_2025.graphml --file1 graphs/dblp_cv_filtered_2022_2025.csv  --file2 graphs/dblp_hri_filtered_2022_2025.csv  --file3 graphs/dblp_sw_filtered_2022_2025.csv

python3 create_bipartite\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_sw_filtered_2022_2025.graphml --outfile tripart2.graphml

python3 overlapping_nodes\ copy.py --graphfile1 graphs/dblp_sw_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml --file1 graphs/dblp_sw_filtered_2022_2025.csv  --file2 graphs/dblp_hri_filtered_2022_2025.csv  --file3 graphs/dblp_dm_filtered_2022_2025.csv

python3 create_bipartite\ copy.py --graphfile1 graphs/dblp_sw_filtered_2022_2025.graphml --graphfile2 graphs/dblp_hri_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml --outfile tripart3.graphml

python3 overlapping_nodes\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_sw_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml --file1 graphs/dblp_cv_filtered_2022_2025.csv  --file2 graphs/dblp_sw_filtered_2022_2025.csv  --file3 graphs/dblp_dm_filtered_2022_2025.csv

python3 create_bipartite\ copy.py --graphfile1 graphs/dblp_cv_filtered_2022_2025.graphml --graphfile2 graphs/dblp_sw_filtered_2022_2025.graphml --graphfile3 graphs/dblp_dm_filtered_2022_2025.graphml --outfile tripart4.graphml