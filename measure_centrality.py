# This is a sample Python script.
import pandas as pd
import networkx as nx
import numpy as np
import argparse
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
np.float_ = np.float64


def centrality_measure(inputfilename,outputfilename):
    G = nx.read_graphml(inputfilename)
    print('nodes',G.number_of_nodes())
    dc = nx.degree_centrality(G)
    cc = nx.closeness_centrality(G)
    bc = nx.betweenness_centrality(G)
    ebc = nx.edge_betweenness_centrality(G)

    # Convert to DataFrame
    df = pd.DataFrame({
        'Name': list(dc.keys()),
        'Degree_Centrality': list(dc.values()),
        'Closeness_Centrality': list(cc.values()),
        'Betweenness_Centrality': list(bc.values())
    })

    # Convert Edge Betweenness Centrality to DataFrame
    df_ebc = pd.DataFrame({
        'Edge': list(ebc.keys()),
        'Edge Betweenness Centrality': list(ebc.values())
    })

    df = df.sort_values(by=['Degree_Centrality'], ascending=False)
    # Display DataFrames
    print("Node Centrality Measures:\n", df)
    print("\nEdge Betweenness Centrality:\n", df_ebc)
    df.to_csv(outputfilename,index = False)


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputfilename",type = str)
    parser.add_argument("--outputfilename",type = str)
    return parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.inputfilename)
    print(inputs.outputfilename)
    centrality_measure(inputs.inputfilename, inputs.outputfilename)
