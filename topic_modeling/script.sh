#python3 yearwise_publish.py --inputfile domains/dblp_sw_filtered_2012_2025.csv

python3 topic_modeling.py --inputfile domains/dblp_sw_filtered_2012_2025.csv --outputfile domains/topics_sw.csv

python3 topic_modeling.py --inputfile domains/dblp_dm_filtered_2012_2025.csv --outputfile domains/topics_dm.csv

python3 topic_modeling.py --inputfile domains/dblp_hri_filtered_2012_2025.csv --outputfile domains/topics_hri.csv

python3 topic_modeling.py --inputfile domains/dblp_cv_filtered_2012_2025.csv --outputfile domains/topics_cv.csv
