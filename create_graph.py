import pandas as pd
from collections import Counter
import networkx as nx
from itertools import permutations,combinations
from tqdm import tqdm
import itertools
import ast
import argparse

def convert_list_to_underscore(names_list):
    if isinstance(names_list, str):  # Convert string to list if necessary
        names_list = ast.literal_eval(names_list)
    return [name.replace(" ", "_") for name in names_list]


def create_graph(inputfilename,outputfilename):
    new_df = pd.read_csv(inputfilename)

    new_df['authors_name'] = new_df['authors_name'].apply(convert_list_to_underscore)

    # new_df['authors_name'] = new_df['authors_name'].apply(ast.literal_eval)
    authors_name_list = new_df['authors_name'].tolist()
    authors_names = list(itertools.chain.from_iterable(authors_name_list))

    G = nx.Graph()
    for author in authors_names:
        G.add_node(author)
    # print(G.nodes)


    for index, row in tqdm(new_df.iterrows(), total=len(new_df)):
        if len(row['authors_name']) > 1:
            lis = row['authors_name']
            timestamp = row['year']
            # print(timestamp)
            list_combinations = list(combinations(lis, 2))
            for edge in list_combinations:
                G.add_edge(edge[0], edge[1],weight = timestamp)
            # break

    print(G.number_of_nodes(), G.number_of_edges())
    # nx.write_weighted_edgelist(G, "dblp_sw_filtered.edgelist")
    nx.write_weighted_edgelist(G, outputfilename)


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputfilename",type = str)
    parser.add_argument("--outputfilename",type = str)
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.inputfilename)
    print(inputs.outputfilename)
    create_graph(inputs.inputfilename, inputs.outputfilename)
