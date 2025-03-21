from html.parser import commentclose

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import os



domainlis = ['sw','cv','dm','hri']

for domain in domainlis:
    file1 = f'subgraphs/University_University_{domain}.graphml'
    file2 = f'subgraphs/University_Research Center_{domain}.graphml'
    file3 = f'subgraphs/University_Company_{domain}.graphml'
    file4 = f'subgraphs/University_Company Research Lab_{domain}.graphml'
    file5 = f'subgraphs/Research Center_Research Center_{domain}.graphml'
    file6 = f'subgraphs/Research Center_Company Research Lab_{domain}.graphml'
    file7 = f'subgraphs/Company_Research Center_{domain}.graphml'
    file8 = f'subgraphs/Company_Company_{domain}.graphml'
    file9 = f'subgraphs/Company_Company Research Lab_{domain}.graphml'
    file10 = f'subgraphs/Company Research Lab_Company Research Lab_{domain}.graphml'

    mainfile = f'graphs_filtered_2022_2025/dblp_{domain}_filtered_2022_2025.graphml'
    G = nx.read_graphml(mainfile)
    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    G1 = nx.read_graphml(file1)
    G2 = nx.read_graphml(file2)
    G3 = nx.read_graphml(file3)
    G4 = nx.read_graphml(file4)
    G5 = nx.read_graphml(file5)
    G6 = nx.read_graphml(file6)
    G7 = nx.read_graphml(file7)
    G8 = nx.read_graphml(file8)
    G9 = nx.read_graphml(file9)
    G10 = nx.read_graphml(file10)

    # lis1 = [(G1.number_of_nodes()/G.number_of_nodes())*100,0,0,0]
    # lis2 = [(G2.number_of_nodes()/G.number_of_nodes())*100,(G3.number_of_nodes()/G.number_of_nodes())*100,0,0]
    # lis3 = [(G4.number_of_nodes()/G.number_of_nodes())*100,(G5.number_of_nodes()/G.number_of_nodes())*100,(G6.number_of_nodes()/G.number_of_nodes())*100,0]
    # lis4 = [(G7.number_of_nodes()/G.number_of_nodes())*100,(G8.number_of_nodes()/G.number_of_nodes())*100,(G9.number_of_nodes()/G.number_of_nodes())*100,(G10.number_of_nodes()/G.number_of_nodes())*100]

    lis1 = [(G1.number_of_nodes()/G.number_of_nodes()),0,0,0]
    lis2 = [(G2.number_of_nodes()/G.number_of_nodes()),(G3.number_of_nodes()/G.number_of_nodes()),0,0]
    lis3 = [(G4.number_of_nodes()/G.number_of_nodes()),(G5.number_of_nodes()/G.number_of_nodes()),(G6.number_of_nodes()/G.number_of_nodes()),0]
    lis4 = [(G7.number_of_nodes()/G.number_of_nodes()),(G8.number_of_nodes()/G.number_of_nodes()),(G9.number_of_nodes()/G.number_of_nodes()),(G10.number_of_nodes()/G.number_of_nodes())]


    mainlist = [lis1,lis2,lis3,lis4]
    data = np.array(mainlist)

    print(data)


    mask = np.triu(np.ones_like(data, dtype=bool))
    # data = np.random.rand(4, 4)
    # Define labels for rows and columns (Optional: Use actual domain names if relevant)
    labels = ["University", "Research Center", "Company", "Company Research Lab"]
    data[data == 0] = np.nan
    # Create the heatmap
    plt.figure(figsize=(10, 7))
    sns.heatmap(data*100,annot=True, cmap="crest", xticklabels=labels, yticklabels=labels, linewidths=0.5)
    # sns.heatmap(np.nan_to_num(data*100, nan=0), annot=True, cmap="crest", fmt='.2f%', xticklabels=labels, yticklabels=labels, linewidths=0.5)

    # sns.heatmap(glue, annot=glue.rank(axis="columns"))
    # plt.yticks(rotation=90)
    if domain == 'cv':
        text = 'Computer Vision'
    elif domain == 'dm':
        text = 'Data Mining'
    elif domain == 'hri':
        text = 'Human Computer Interaction'
    elif domain == 'sw':
        text = 'Software Engineering'
    plt.title(f"Collaboration between Different Category Institutions in {text}")

    filename = str(text) + '.pdf'
    for text in plt.gca().texts:
        text.set_text(text.get_text() + "%")

    # plt.tight_layout()

    plt.savefig(filename)
    # plt.show()