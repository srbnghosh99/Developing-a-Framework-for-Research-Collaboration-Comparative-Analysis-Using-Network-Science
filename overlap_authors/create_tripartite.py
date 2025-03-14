import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations

import argparse


def draw_tripart(graphfile1, graphfile2, graphfile3,outfile):
    # Load the two domain graphs
    domain1 = nx.read_graphml(graphfile1)
    domain2 = nx.read_graphml(graphfile2)
    domain3 = nx.read_graphml(graphfile3)

    # Load the dataframe containing paper counts
    df = pd.read_csv("test.csv") # Columns: Author, Domain1_Count, Domain2_Count
    # df1 = df1.head(25)
    # df2 = pd.read_csv("test2.csv")
    # df2 = df2.head(25)

    # Create a bipartite graph
    B = nx.Graph()
    df['avg_degree'] = df[['Degree1', 'Degree2', 'Degree3']].mean(axis=1)
    domain1_node = "CV"
    domain2_node = "HRI"
    domain3_node = "DM"
    B.add_node(domain1_node, bipartite=0, size=2000)
    B.add_node(domain2_node, bipartite=0, size=2000)
    B.add_node(domain3_node, bipartite=0, size=2000)

    # Add common authors as middle layer nodes
    # df = df.sort_values(by=['papers_count1'], ascending=False)
    for _, row in df.iterrows():
        author = row['Node']
        paper_count1 = row["papers_count1"]
        paper_count2 = row["papers_count2"]
        paper_count3 = row["papers_count3"]
        degree = row['avg_degree']
        # degree2 = row['Degree_y']
        # total_papers = row["Total_Count"]

        B.add_node(author, bipartite=1, size=degree * 20)  # Scale node size by paper count
        B.add_edge(domain1_node, author, weight=paper_count1)
        B.add_edge(domain2_node, author, weight=paper_count2)
        B.add_edge(domain3_node, author, weight=paper_count3)


    # Draw the bipartite graph
    # pos = nx.bipartite_layout(B, nodes=[domain1_node, domain2_node])
    # nx.draw(B, pos, with_labels=True, node_size=[B.nodes[n]['size'] for n in B.nodes],
    #         edge_color='gray', width=[B.edges[e]['weight'] / 10 for e in B.edges])
    # plt.show()

    print(B.degree())
    nx.write_graphml(B,outfile)


def parse_args():
    parser = argparse.ArgumentParser(description="Process ORCID XML Files")
    parser.add_argument("--graphfile1", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--graphfile2", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--graphfile3", type=str, required=True, help="Path to input graph file")
    # parser.add_argument("--file", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--outfile", type=str, required=True, help="Path to input CSV file")
    return parser.parse_args()


if __name__ == '__main__':
    inputs = parse_args()
    # print(f"📂 Processing ORCID data from: {inputs.filepath}")
    draw_tripart(inputs.graphfile1, inputs.graphfile2, inputs.graphfile3,inputs.outfile)
