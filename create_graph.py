import pandas as pd
from collections import Counter
import networkx as nx
from itertools import permutations,combinations
from tqdm import tqdm
import itertools
import ast


G = nx.Graph()
import ast

new_df = pd.read_csv('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/data/dblp_sw_filtered.csv')
new_df['authors_name'] = new_df['authors_name'].apply(ast.literal_eval)
authors_name_list = new_df['authors_name'].tolist()
authors_names = list(itertools.chain.from_iterable(authors_name_list))
G = nx.Graph()
for author in authors_names:
    G.add_node(author)
#for index, row in new_df.iterrows():
for index, row in tqdm(new_df.iterrows(), total=len(new_df)):
    # G.add_node(row['authors_name']):
    #new_df['authors_name'] = new_df['authors_name'].apply(ast.literal_eval)
    for index, row in new_df.iterrows():
        if len(row['authors_name']) > 1:
            lis = row['authors_name']
            list_combinations = list(combinations(lis, 2))
            # print(list_combinations)
            for edge in list_combinations:
                # print(edge[0],edge[1])
                G.add_edge(edge[0], edge[1])
            # break
print(G.number_of_nodes(), G.number_of_edges())


