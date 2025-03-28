import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import ast
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def topic_shift(file1, file2,file3,outfile,outgraph):
    # df = pd.read_csv('dblp_dm_filtered_2012_2025.csv')
    df = pd.read_csv(file1)
    df['authors_name'] = df['authors_name'].apply(ast.literal_eval)
    # info_df = pd.read_csv('dm2.csv')
    info_df = pd.read_csv(file2)
    info_df = info_df.rename(columns={'title_topic': 'Topic'})

    # topics_info = pd.read_csv('topics_dm2.csv')
    topics_info = pd.read_csv(file3)
    topics_info = topics_info[['Topic','Name']]
    # topics_info = topics_info.rename(columns={'Topic': 'title_topic'})
    info_df = info_df.merge(topics_info, on = 'Topic', how = 'left')
    info_df = info_df[['title','Topic','Name']]

    new_df = df.merge(info_df, on = 'title', how='left')
    new_df = new_df[['authors_name', 'title', 'Topic','Name' ,'year']]
    print(new_df)
    # new_df = new_df['Topic'].fillna(0)
    print(new_df['Topic'])
    new_df['Topic'] = new_df['Topic'].astype('Int64')


    authornameList = []
    titleList = []
    NameList = []
    yearList = []

    for index, row in new_df.iterrows():
        names = row['authors_name']
        if len(names) > 1:
            for name in names:
                authornameList.append(name)
                titleList.append(row['Topic'])
                NameList.append(row['Name'])
                yearList.append(row['year'])


    dynamic_df = pd.DataFrame({
                'Author':authornameList,
                'Topic': titleList,
                'Name': NameList,
                'year': yearList
            })

    dynamic_df = dynamic_df[dynamic_df['Topic'] != -1]

    print(dynamic_df)
    author_topic_map = dynamic_df.groupby(['Author','year'])['Name'].agg(lambda x: x.mode()[0]).reset_index()
    print(author_topic_map)
    # author_topic_map.to_csv('topic_shift_dm.csv')
    author_topic_map.to_csv(outfile)

    # Create a directed graph to show transitions
    # df = pd.read_csv('topic_shift_dm.csv')
    # G = nx.DiGraph()
    #
    # for _, row in df.iterrows():
    #     G.add_edge(f"{row['year']}_{row['Name']}", f"{row['year']+1}_{row['Name']}", weight=1)
    #
    # # Draw the network graph
    # nx.write_graphml(G,'topic_transit.graphml')
    # pos = nx.spring_layout(G, seed=42)
    # nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10)
    # plt.title("Topic Transition Network")

    # plt.show()



    # Sample data (Author, Year, Topic)
    # data = [
    #     ("A. Aziz Altowayan", 2016, "Sentiment Analysis"),
    #     ("A. Aziz Altowayan", 2017, "Sentiment Analysis"),
    #     ("A. B. M. Moniruzzaman", 2019, "Graph Neural Networks"),
    #     ("A. B. Siddique 0001", 2020, "Neural Text Retrieval"),
    #     ("A. B. Siddique 0001", 2021, "Action Recognition"),
    #     ("A. B. Siddique 0001", 2022, "Task-Oriented Dialogue"),
    #     ("A. B. Siddique 0001", 2023, "Mobile Applications")
    # ]

    df = pd.read_csv(outfile)

    print('Unique topics,', df['Name'].nunique())

    def clean_topic(name):
        # Extracting meaningful words from the topic field (splitting by underscores and spaces)
        words = name.split('_')
        return ' '.join(words[:3])  # Taking the first three words as a meaningful topic

    # Convert DataFrame to list of tuples
    data = [(row['Author'], row['year'], (row['Name'])) for _, row in df.iterrows()]

    # Create a directed graph
    G = nx.DiGraph()

    nodelist = (df['Name'].unique().tolist())
    # for node in nodelist:
    #     G.add_node(node, bipartite=0, size=200)
    # print(G.number_of_nodes())
    # print(G.nodes())

    #
    # # Add edges representing transitions between topics
    # for i in range(len(data) - 1):
    #     # print(data[i][0],data[i][1],data[i][2])
    #     # break
    #     if data[i][0] == data[i+1][0] and data[i][1] != data[i+1][1]:  # Ensure it's the same author and different year
    #         # G.add_edge(f"{data[i][1]}: {data[i][2]}", f"{data[i+1][1]}: {data[i+1][2]}", author=data[i][0])
    #         G.add_edge(f"{data[i][1]}: {data[i][2]}", f"{data[i + 1][1]}")
    #         # G.add_edge(data[i][2], data[i+1][2], weight=data[i+1][1])

    for i in range(len(data) - 1):
        if data[i][0] == data[i+1][0] and data[i][1] != data[i+1][1] and data[i][2] != data[i+1][2]:  # Ensure it's the same author
            source = f"{data[i][1]}: {data[i][2]}"
            target = f"{data[i+1][1]}: {data[i+1][2]}"

            if G.has_edge(source, target):
                G[source][target]['weight'] += 1  # Increase weight if edge exists
            else:
                G.add_edge(source, target, weight=1)  # Add new edge with weight 1
    print(G.number_of_nodes(),G.number_of_edges())
    # Draw the graph
    # plt.figure(figsize=(10, 6))
    # pos = nx.spring_layout(G, seed=42, k=0.5)  # Adjust layout
    #
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight="bold", arrows=True)
    #
    # plt.title("Topic Flow of Authors Over Time", fontsize=14)
    # plt.show()

    nx.write_graphml(G,outgraph)


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--file1", type=str)
    parser.add_argument("--file2", type=str)
    parser.add_argument("--file3", type=str)
    parser.add_argument("--outfile", type=str)
    parser.add_argument("--outgraph", type=str)
    return parser.parse_args()


def main():
    inputs = parse_args()
    print(inputs.file1)
    print(inputs.file2)
    print(inputs.file3)
    print(inputs.outfile)
    print(inputs.outgraph)
    topic_shift(inputs.file1, inputs.file2,inputs.file3,inputs.outfile,inputs.outgraph)


if __name__ == '__main__':
    main()
