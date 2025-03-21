import networkx as nx
import matplotlib.pyplot as plt
import argparse

# Assuming you already have your full graph 'G'
def draw_subgraph(subgraph, title):
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12)
    plt.title(title)
    plt.show()

# Create subgraphs based on affiliation type


'''
# Filter edges: between universities or university and nodes with no affiliation
uni_uni_edges = [(u, v) for u, v, d in G.edges(data=True) if
                 ('University' in G.nodes[u].get('affiliation', '') and 'University' in G.nodes[v].get('affiliation', ''))]
                 # ('University' in G.nodes[u].get('affiliation', '') and '' == G.nodes[v].get('affiliation', '')) or
                 # ('University' in G.nodes[v].get('affiliation', '') and '' == G.nodes[u].get('affiliation', ''))]

# print(uni_uni_edges)

uni_uni_subgraph = G.subgraph([u for u, v in uni_uni_edges] + [v for u, v in uni_uni_edges])
# uni_uni_subgraph
nx.write_graphml(uni_uni_subgraph,'uni_uni_subgraph.graphml')
largest_cc_nodes = max(nx.connected_components(uni_uni_subgraph), key=len)
largest_cc_subgraph = G.subgraph(largest_cc_nodes)
nx.write_graphml(largest_cc_subgraph,'uni_uni_subgraph_largestcc.graphml')

'''
def create_subgraph(inputgraph,outputgraph):

    G = nx.read_graphml(inputgraph)
    # print(flag)
    # flag = int(flag)

    # if flag == 1:
    #     rc_rc_edges = [(u, v) for u, v, d in G.edges(data=True) if
    #                      ('University' in G.nodes[u].get('affiliation', '') and 'Research Center' in G.nodes[v].get('affiliation', '')) or
    #     ('Research Center' in G.nodes[u].get('affiliation', '') and 'University' in G.nodes[v].get('affiliation', ''))]
    # if flag == 2:
    #
    #     rc_rc_edges = [(u, v) for u, v, d in G.edges(data=True) if
    #                      ('University' in G.nodes[u].get('affiliation', '') and 'Company' in G.nodes[v].get('affiliation', '')) or
    #     ('Company' in G.nodes[u].get('affiliation', '') and 'University' in G.nodes[v].get('affiliation', ''))]
    #
    # if flag == 3:
    #     rc_rc_edges = [(u, v) for u, v, d in G.edges(data=True) if
    #                      ('Company' in G.nodes[u].get('affiliation', '') and 'Research Center' in G.nodes[v].get('affiliation', '')) or
    #     ('Research Center' in G.nodes[u].get('affiliation', '') and 'Company' in G.nodes[v].get('affiliation', ''))]
    #

    affiliations = {
        1: ("University","University"),
        2: ("University", "Research Center"),
        3: ("University", "Company"),
        4: ("University", "Company Research Lab"),
        5: ("Company", "Company"),
        6: ("Company", "Research Center"),
        7: ("Company", "Company Research Lab"),
        8: ("Research Center", "Research Center"),
        9: ("Research Center", "Company Research Lab"),
        10: ("Company Research Lab", "Company Research Lab"),
    }

    # if flag in affiliations:
    for key in affiliations:
        aff1, aff2 = affiliations[key]
        rc_rc_edges = [(u, v) for u, v, d in G.edges(data=True) if
                       (aff1 in G.nodes[u].get('affiliation', '') and aff2 in G.nodes[v].get('affiliation', '')) or
                       (aff2 in G.nodes[u].get('affiliation', '') and aff1 in G.nodes[v].get('affiliation', ''))]

        rc_rc_subgraph = G.subgraph([u for u, v in rc_rc_edges] + [v for u, v in rc_rc_edges])
        # uni_uni_subgraph
        name = 'subgraphs/' + aff1 + '_' +aff2 + '_'+outputgraph
        nx.write_graphml(rc_rc_subgraph,name)
# largest_cc_nodes = max(nx.connected_components(rc_rc_subgraph), key=len)
# largest_cc_subgraph = G.subgraph(largest_cc_nodes)
# nx.write_graphml(largest_cc_subgraph,'rc_rc_subgraph_largestcc.graphml')

def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputgraph",type = str)
    # parser.add_argument("--Option", type=str)
    parser.add_argument("--outputgraph",type = str)
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    print(inputs.inputgraph)
    # print(inputs.Option)
    create_subgraph(inputs.inputgraph,inputs.outputgraph)
    # draw_subgraph(inputs.inputfilename, inputs.outputfilename)