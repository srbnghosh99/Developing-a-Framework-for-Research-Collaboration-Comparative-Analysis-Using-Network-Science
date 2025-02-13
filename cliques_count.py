
import networkx as nx
import pandas as pd
import argparse

def largest_connected_component(G):
    # Find all connected components
    components = list(nx.connected_components(G))
    
    # Find the largest component
    largest_component = max(components, key=len)
    
    return list(largest_component)

def cliques_by_size(G):
    # Find all cliques in the graph
    cliques = list(nx.find_cliques(G))
    
    # Initialize an empty dictionary
    cliques_dict = {}
    
    # Loop through each clique
    for cliq in cliques:
        size = len(cliq)
        
        # If the size is not already a key in the dictionary, add it with an empty list
        if size not in cliques_dict:
            cliques_dict[size] = []
        
        # Append the clique to the list corresponding to its size
        cliques_dict[size].append(cliq)
    
    return cliques_dict


def find_cliques(inputfilename,outputfilename):
    G = nx.read_graphml(inputfilename)
    connected_components = list(nx.connected_components(G))
    num_connected_components = len(connected_components)

    # Compute cliques count
    cliques = list(nx.find_cliques(G))  # List of all maximal cliques
    num_cliques = len(cliques)

    print(f"Number of Connected Components: {num_connected_components}")
    print(f"Number of Cliques: {num_cliques}")

    size_of_cliques = []
    size_of_components = []

    for cliq in connected_components:
        size_of_components.append(len(cliq))
        # size_of_cliques.append(len(cliq))
    print(max(size_of_components),min(size_of_components))


    for cliq in cliques:
        size_of_cliques.append(len(cliq))
    print(max(size_of_cliques),min(size_of_cliques))


    cliques_dict = cliques_by_size(G)
    # print(cliques_dict)
    data = []
    for size, cliques in cliques_dict.items():
        for cliq in cliques:
            data.append((size, cliq))

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Clique Size', 'Clique'])
    # df = pd.DataFrame.from_dict(cliques_dict)
    print(df)
    df.to_csv(outputfilename)

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputfilename",type = str)
    parser.add_argument("--outputfilename",type = str)
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.inputfilename)
    print(inputs.outputfilename)
    find_cliques(inputs.inputfilename, inputs.outputfilename)