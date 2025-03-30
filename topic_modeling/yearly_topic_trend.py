import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import numpy as np
from matplotlib.ticker import MaxNLocator
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def create_topic_shift(graphfile,outfile):
    # graph = nx.read_graphml('topic_transit_sw.graphml')
    graph = nx.read_graphml(graphfile)
    nodes = list(graph.nodes())
    df =pd.DataFrame(nodes, columns=['NAME'])


    nodename = []
    indeg = []
    outdeg = []

    for node in graph.nodes():
        nodename.append(node)
        indeg.append(graph.in_degree(node))
        outdeg.append(graph.out_degree(node))


    new_df = pd.DataFrame({'Node':nodename,'Indegree':indeg,'Outdegree':outdeg})

    new_df['topic_shift'] =  new_df['Indegree'] - new_df['Outdegree']
    new_df["Year"] = new_df["Node"].str.split(":").str[0].astype(int)
    new_df["Node"] = new_df["Node"].str.split(": ").str[1]
    new_df["Topic"] = new_df["Node"].str.split("_").str[0]
    # new_df["Node"] = new_df["Node"].str.split(": ").str[1]
    # new_df["Node"] = new_df["Node"].astype(str).str.split('_').str[:2].str.join('_')
    # new_df['shortened_topics'] = new_df['Node'].apply(lambda x: '_'.join(x.split('_')[:2]))
    new_df["shortened_topics"] = new_df["Node"].astype(str).str.split('_').str[0] + '_' + new_df["Node"].astype(str).str.split('_').str[1]
    new_df.to_csv(outfile)

def topic_trends(file):

    new_df = pd.read_csv(file)
    plt.figure(figsize=(12, 6))
    print(new_df['Topic'].nunique())
    for i in range(0,10):
        data = new_df[new_df['Topic'] == i].reset_index()
        print(data)
        if data.empty:
            continue  # Skip if no data for this topic
        topic = data['Node'][0]
        data = data.sort_values(by='Year', ascending=True)
        years = data['Year'].tolist()
        topic_shifts = data['topic_shift'].tolist()

        plt.plot(years, topic_shifts, marker='o', linestyle='-', label=f"{topic}")

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("Topic Shift")
    plt.title("Topic Shift Over Time for 10 Topics")

    # Show grid and legend
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Adjust legend outside
    plt.tight_layout()

    # Show plot
    plt.show()

    new_df = new_df.sort_values(by='topic_shift',ascending = False)
    new_df = new_df[new_df['topic_shift'] > 2 ]
    new_df = new_df.head(200)
    years = new_df["Year"].tolist()
    topic_shifts = new_df['topic_shift'].tolist()
    topics = new_df['shortened_topics'].tolist()


    jitter_strength = 1.75 # Adjust this value based on your needs
    jittered_topic_shifts = [y + np.random.normal(0, jitter_strength) for y in topic_shifts]

    plt.figure(figsize=(30, 9))
    sns.scatterplot(x=years, y=jittered_topic_shifts, color='blue', marker='o', s=10)


    # Add annotations (text labels)
    for i, txt in enumerate(topics):
        plt.annotate(txt, (years[i], jittered_topic_shifts[i]), fontsize=7, xytext=(5, 5), textcoords='offset points')

    plt.axhline(0, color='gray', linestyle='dashed')
    plt.legend().set_visible(False)
    plt.xlim(min(years), max(years) + 1)
    # Set tighter x-axis ticks
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=len(set(years))))  # Adjust the number of bins
    plt.xticks(sorted(set(years)))  # Make sure only unique years are displayed

    plt.xlabel("Year")
    plt.ylabel("Topic Shift")
    plt.title("Topic Shift Over Time")
    plt.tight_layout()
    # plt.savefig('test.pdf')
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--graphfile", type=str)
    parser.add_argument("--file", type=str)
    parser.add_argument("--outfile", type=str)
    return parser.parse_args()


def main():
    inputs = parse_args()
    print(inputs.file)
    create_topic_shift(inputs.graphfile,inputs.outfile)
    # topic_trends(inputs.file)


if __name__ == '__main__':
    main()

