import networkx as nx
import pandas as pd
import argparse

def centrality(graphfile,outfile):
    graphfile = "graphs_filtered_2022_2025/dblp_cv_filtered_2022_2025.graphml"
    G = nx.read_graphml(graphfile)
    print(G.number_of_nodes(),G.number_of_edges())
    # Get the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)

    # Create a subgraph containing only nodes from the largest connected component
    G_largest_cc = G.subgraph(largest_cc).copy()
    print(G_largest_cc.number_of_nodes(),G_largest_cc.number_of_edges())
    pagerank_scores = nx.pagerank(G_largest_cc)
    # print(pagerank_scores)
    print('done')
    betweenness = nx.betweenness_centrality(G_largest_cc)
    print('done')
    closeness = nx.closeness_centrality(G_largest_cc)
    print('done')
    eigenvector = nx.eigenvector_centrality(G_largest_cc)
    print('done')
    centrality_df = pd.DataFrame({'Node': list(G_largest_cc.nodes), 'Betweenness': betweenness.values(), 'Closeness': closeness.values(), 'Eigenvector': eigenvector.values(),'Pagerank':pagerank_scores.values()})
    print(centrality_df)


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputgraph",type = str)
    # parser.add_argument("--Option", type=str)
    parser.add_argument("--outfile",type = str)
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.inputgraph)
    print(inputs.Option)
    centrality(inputs.inputgraph,inputs.outfile)
    # draw_subgraph(inputs.inputfilename, inputs.outputfilename)