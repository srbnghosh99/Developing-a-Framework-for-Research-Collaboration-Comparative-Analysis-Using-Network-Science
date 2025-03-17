import networkx as nx
import argparse
import pandas as pd
import create_tripartite
def check_digits(text):
    return any(char.isdigit() for char in text)

def normalize_name(name):
    return name.replace(' ', '_')

def func(graphfile1,graphfile2,graphfile3,file1,file2,file3,outfile):
    with open("output.txt", "r+") as file:
        content = file.read()
        file.write(f'\n')
        file.write(f'-------------------------------------------\n')
        # file.write("This text will be written to the file.")
        # file.write(content[len("New content to overwrite the beginning."):])
        # Load graphs
        G1 = nx.read_graphml(graphfile1)
        G2 = nx.read_graphml(graphfile2)
        G3 = nx.read_graphml(graphfile3)
        # G4 = nx.read_graphml(graphfile4)
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        df3 = pd.read_csv(file3)
        # df4 = pd.read_csv(file4)
        # print('{} nodes and edges',G1.number_of_nodes(),G1.number_of_edges())
        # print('G2', G2.number_of_nodes(), G2.number_of_edges())
        file.write(f'{file1} nodes and edges: {G1.number_of_nodes()} and {G1.number_of_edges()} \n')
        file.write(f'{file2} nodes and edges: {G2.number_of_nodes()} and {G2.number_of_edges()} \n')
        file.write(f'{file3} nodes and edges: {G3.number_of_nodes()} and {G3.number_of_edges()} \n')
        # file.write(f'{file4} nodes and edges: {G4.number_of_nodes()} and {G4.number_of_edges()} \n')
        # G3 = nx.read_graphml("/Users/shrabanighosh/PycharmProjects/orcid_extract/untitled folder/dblp_hri_filtered_2022_2025.graphml")
        # Find common nodes across all three graphs
        common_nodes = set(G1.nodes()) & set(G2.nodes()) & set(G3.nodes())

        normalized_G1 = {normalize_name(node): node for node in G1.nodes()}
        normalized_G2 = {normalize_name(node): node for node in G2.nodes()}
        normalized_G3 = {normalize_name(node): node for node in G3.nodes()}
        # normalized_G4 = {normalize_name(node): node for node in G4.nodes()}
        # normalized_G3 = {normalize_name(node): node for node in G3.nodes()}

        # Find common normalized names
        common_normalized_names = (set(normalized_G1.keys()) & set(normalized_G2.keys())  & set(normalized_G3.keys()))
        df3 = pd.read_csv('domains/Computer_Vision.csv')
        df4 = pd.read_csv('domains/Human_Robot_Interaction.csv')
        df5 = pd.read_csv('domains/Software_Engineering.csv')
        lis = []
        matched_count = 0
        for name in common_normalized_names:
            node1, node2, node3 = normalized_G1[name], normalized_G2[name], normalized_G3[name]
            if node1 == node2:
                others1 = df3[df3['authors_name'].str.contains(node1)]
                others2 = df4[df4['authors_name'].str.contains(node1)]
                others3 = df5[df5['authors_name'].str.contains(node1)]
                # print(others['authors_name'].tolist())
                if (others1['authors_name'].tolist() == 1 or others2['authors_name'].tolist() == 1 or others3['authors_name'].tolist() == 1):
                    lis.append(node1)
                    print(node1, node2)
                    matched_count += 1
                elif check_digits(node1):
                    lis.append(node1)
                    print(node1, node2)
                    matched_count += 1
                else:
                    continue

        for node in common_nodes:
            attrs1, attrs2, attrs3= G1.nodes[node], G2.nodes[node], G3.nodes[node]
            if len(attrs1) != 0:
                if attrs1 == attrs2 == attrs3:
                    lis.append(node)
                    # print(len(attrs1))
                    # print(node, attrs1, attrs2)
                    matched_count += 1

        # print('Total number of common users',matched_count)
        file.write(f'Total number of common users:  {matched_count} \n')
        file.close()


        # Get degree information
        degree_data1 = dict(G1.degree(lis))
        degree_data2 = dict(G2.degree(lis))
        degree_data3 = dict(G3.degree(lis))
        # degree_data4 = dict(G4.degree(lis))

        # Convert to DataFrame
        df_degree1 = pd.DataFrame(degree_data1.items(), columns=['Node', 'Degree1'])
        df_degree2 = pd.DataFrame(degree_data2.items(), columns=['Node', 'Degree2'])
        df_degree3 = pd.DataFrame(degree_data3.items(), columns=['Node', 'Degree3'])
        # df_degree4 = pd.DataFrame(degree_data4.items(), columns=['Node', 'Degree4'])
        # df_degree2 = df_degree1.sort_values(by=['Degree'],ascending = False)

        df_degree1['papers_count1'] = ''
        papers = []
        for index, row in df_degree1.iterrows():
            name = row['Node']
            papers_count = df1[df1['authors_name'].str.contains(name)].shape[0]
            # print(papers_count)
            papers.append(papers_count)
        df_degree1['papers_count1'] = papers
        df_degree1 = df_degree1.sort_values(by=['papers_count1'], ascending=False)
        # df_degree1.to_csv('test1.csv')

        df_degree2['papers_count2'] = ''
        papers = []
        for index, row in df_degree2.iterrows():
            name = row['Node']
            papers_count = df2[df2['authors_name'].str.contains(name)].shape[0]
            # print(papers_count)
            papers.append(papers_count)
        df_degree2['papers_count2'] = papers
        df_degree2 = df_degree2.sort_values(by=['papers_count2'], ascending=False)
        # df_degree2.to_csv('test2.csv')

        df_degree3['papers_count3'] = ''
        papers = []
        for index, row in df_degree3.iterrows():
            name = row['Node']
            papers_count = df3[df3['authors_name'].str.contains(name)].shape[0]
            # print(papers_count)
            papers.append(papers_count)
        df_degree3['papers_count3'] = papers
        df_degree3 = df_degree3.sort_values(by=['papers_count3'], ascending=False)
        # df_degree1.to_csv('test1.csv')

        # df_degree4['papers_count4'] = ''
        # papers = []
        # for index, row in df_degree4.iterrows():
        #     name = row['Node']
        #     papers_count = df4[df4['authors_name'].str.contains(name)].shape[0]
        #     # print(papers_count)
        #     papers.append(papers_count)
        # df_degree4['papers_count4'] = papers
        # df_degree4 = df_degree4.sort_values(by=['papers_count4'], ascending=False)

        # merge_df = df_degree1.merge(df_degree2,on='Node',how='inner')
        # merge_df = pd.merge(pd.merge(pd.merge(df_degree1, df_degree2, on='Node', how='inner'), df_degree3, on='Node', how='inner'), df_degree4, on='Node', how='inner')
        merge_df = pd.merge(pd.merge(df_degree1, df_degree2, on='Node', how='inner'), df_degree3, on='Node', how='inner')

        # merge_df = merge_df.merge(df_degree3, on='Node', how='inner')
        # merge_df = merge_df.merge(df_degree4, on='Node', how='inner')

        print(merge_df)
        merge_df.to_csv('test.csv')

        create_tripartite.draw_tripart(graphfile1, graphfile2, graphfile3,outfile)

        # print(df_degree1,df_degree2)

def parse_args():
    parser = argparse.ArgumentParser(description="Process ORCID XML Files")
    parser.add_argument("--graphfile1", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--graphfile2", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--graphfile3", type=str, required=True, help="Path to input graph file")
    # parser.add_argument("--graphfile4", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--file1", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--file2", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--file3", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--outfile", type=str, required=True, help="Path to input CSV file")
    # parser.add_argument("--file4", type=str, required=True, help="Path to input CSV file")
    # parser.add_argument("--outfile", type=str, required=True, help="Path to input CSV file")
    return parser.parse_args()

if __name__ == '__main__':
    inputs = parse_args()
    # print(f"📂 Processing ORCID data from: {inputs.filepath}")
    func(inputs.graphfile1,inputs.graphfile2,inputs.graphfile3,inputs.file1,inputs.file2,inputs.file3,inputs.outfile)