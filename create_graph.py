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

        names_list = ['DA' if x != x else x for x in names_list]
        print(names_list)
        names_list = ast.literal_eval(names_list)
        # print(names_list)
    return [name.replace(" ", "_") for name in names_list]


def create_graph(inputfilename,outputfilename):
    new_df = pd.read_csv(inputfilename)
    # print(new_df)
    # new_df['authors_ins'] = new_df['authors_ins'].apply(convert_list_to_underscore)

    new_df['authors_name'] = new_df['authors_name'].apply(ast.literal_eval)
    authors_name_list = new_df['authors_name'].tolist()
    authors_names = list(itertools.chain.from_iterable(authors_name_list))

    new_df['authors_orcid'] = new_df['authors_orcid'].apply(ast.literal_eval)
    authors_orcid_list = new_df['authors_orcid'].tolist()
    authors_orcids = list(itertools.chain.from_iterable(authors_orcid_list))

    new_df['authors_aff'] = new_df['authors_aff'].apply(ast.literal_eval)
    authors_orcid_list = new_df['authors_aff'].tolist()
    authors_aff = list(itertools.chain.from_iterable(authors_orcid_list))

    new_df['authors_ins'] = new_df['authors_ins'].apply(ast.literal_eval)
    print(new_df['authors_ins'][0][0])
    authors_orcid_list = new_df['authors_ins'].tolist()
    authors_inst = list(itertools.chain.from_iterable(authors_orcid_list))

    G = nx.Graph()
    for author, orcid, aff, inst in zip(authors_names, authors_orcids, authors_aff, authors_inst):
        node_attrs = {
            "orcid_id": orcid if orcid != "DA" else "",
            "affiliation": aff if aff != "DA" else "",
            "institution": inst if inst != "DA" else ""
        }
        G.add_node(author, **node_attrs)

    # for author,orcid,aff,inst in zip(authors_names,authors_orcids,authors_aff,authors_inst):
    #     if orcid !='DA' and aff != 'DA' and inst != 'DA' :
    #         G.add_node(author, orcid_id = orcid, affiliation = aff, institution = inst)
    #     elif orcid !='DA' and aff == 'DA':
    #         G.add_node(author, orcid_id=orcid, affiliation = '')
    #     elif aff !='DA' and orcid == 'DA':
    #         G.add_node(author,orcid_id = '' ,affiliation = aff)
    #     else:
    #         G.add_node(author,orcid_id = '',affiliation = '')
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

    print("Number of nodes",G.number_of_nodes())
    print("Number of edges",G.number_of_edges())
    # nx.write_weighted_edgelist(G, "dblp_sw_filtered.edgelist")
    # nx.write_weighted_edgelist(G, outputfilename)
    nx.write_graphml(G, outputfilename)
    for node in G.nodes(data=True):
        print(node)
        # break
    # loaded_graphml = nx.read_graphml(outputfilename)
    # print(loaded_graphml.nodes(data=True))


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
