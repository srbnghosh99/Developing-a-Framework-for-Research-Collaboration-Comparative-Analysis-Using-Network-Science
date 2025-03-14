import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations

# Load the two domain graphs
domain1 = nx.read_graphml("graphs/dblp_dm_filtered_2022_2025.graphml")
domain2 = nx.read_graphml("graphs/dblp_sw_filtered_2022_2025.graphml")

# Load the dataframe containing paper counts
df = pd.read_csv("test.csv") # Columns: Author, Domain1_Count, Domain2_Count
# df1 = df1.head(25)
# df2 = pd.read_csv("test2.csv")
# df2 = df2.head(25)

# Create a bipartite graph
B = nx.Graph()

domain1_node = "Domain1"
domain2_node = "Domain2"
B.add_node(domain1_node, bipartite=0, size=2000)
B.add_node(domain2_node, bipartite=0, size=2000)

# Add common authors as middle layer nodes
df = df.sort_values(by=['papers_count1'], ascending=False)
for _, row in df.head(25).iterrows():
    author = row['Node']
    paper_count1 = row["papers_count1"]
    paper_count2 = row["papers_count2"]
    degree = row['Degree_x']
    # degree2 = row['Degree_y']
    # total_papers = row["Total_Count"]

    B.add_node(author, bipartite=1, size=degree * 2)  # Scale node size by paper count
    B.add_edge(domain1_node, author, weight=paper_count1)
    B.add_edge(domain2_node, author, weight=paper_count2)

df = df.sort_values(by=['papers_count2'], ascending=False)
for _, row in df.head(26).iterrows():
    author = row['Node']
    paper_count1 = row["papers_count1"]
    paper_count2 = row["papers_count2"]
    degree = row['Degree_y']


    B.add_node(author, bipartite=1, size=degree * 2)  # Scale node size by paper count
    B.add_edge(domain1_node, author, weight=paper_count1)
    B.add_edge(domain2_node, author, weight=paper_count2)

# Draw the bipartite graph
# pos = nx.bipartite_layout(B, nodes=[domain1_node, domain2_node])
# nx.draw(B, pos, with_labels=True, node_size=[B.nodes[n]['size'] for n in B.nodes],
#         edge_color='gray', width=[B.edges[e]['weight'] / 10 for e in B.edges])
# plt.show()

print(B.degree())
nx.write_graphml(B,'bipart1.graphml')