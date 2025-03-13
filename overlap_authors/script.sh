#python3 parsexml_orcid.py --filepath 0000-0001-5749-3000.xml
#python3 parsexml_orcid.py --filepath 0009-0008-3019-1000.xml
#python3 parsexml_orcid.py --filepath 0000-0002-0999-4000.xml
#python3 parsexml_orcid.py --filepath 0000-0001-9918-3000.xml


#!/bin/bash

directory="/Users/shrabanighosh/PycharmProjects/orcid_extract/graphs"  # Replace with actual path
files=($(ls "$directory"))

for ((i=0; i<${#files[@]}; i++)); do
    for ((j=i+1; j<${#files[@]}; j++)); do
        if [[ ${files[i]} == *.graphml && ${files[j]} == *.graphml ]]; then
            python overlapping_nodes.py --graphfile1 "$directory/${files[i]}" --graphfile2 "$directory/${files[j]}"
        fi
#        python overlapping_nodes.py --graphfile1 "$directory/${files[i]}" --graphfile2 "$directory/${files[j]}"
    done
done