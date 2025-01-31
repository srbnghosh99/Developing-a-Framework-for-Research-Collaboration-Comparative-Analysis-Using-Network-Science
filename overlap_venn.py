# Sample Data
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn3

# Load data
df1 = pd.read_csv("/Users/shrabanighosh/UNCC/Spring 2025/scholar data/centrality/hci.csv")
df2 = pd.read_csv("/Users/shrabanighosh/UNCC/Spring 2025/scholar data/centrality/cv.csv")
df3 = pd.read_csv("/Users/shrabanighosh/UNCC/Spring 2025/scholar data/centrality/sw.csv")
df4 = pd.read_csv("/Users/shrabanighosh/UNCC/Spring 2025/scholar data/centrality/dm.csv")

# List of centrality measures
cen = ['Degree_Centrality', 'Closeness_Centrality', 'Betweenness_Centrality']
df1 = df1.sort_values(by=cen,ascending = False)
df2 = df2.sort_values(by=cen,ascending = False)
df3 = df3.sort_values(by=cen,ascending = False)
df4 = df4.sort_values(by=cen,ascending = False)

domains = ["Human Computer Interaction", "Computer Vision", "Software Engineering", "Data Mining"]
# domains = [hci,cv,sw,dm]
dfs = [df1, df2, df3, df4]
domain_sets = {domain: set() for domain in domains}  # Initialize empty sets for each domain
# Extract top 10 researchers for each centrality measure
for centrality in cen:
    for domain, df in zip(domains, dfs):
        df_sorted = df.sort_values(by=cen, ascending=False)
        top_researchers = set(df_sorted['Name'].iloc[:50])  # Convert top 10 to set
        domain_sets[domain].update(top_researchers)  # Add to set for the domain

    # Select only three domains for venn3 (since venn4 is not supported)
    selected_domains = list(domain_sets.keys())[1:4]
    selected_sets = [domain_sets[domain] for domain in selected_domains]

    print(selected_domains)
    # Plot Venn diagram
    plt.figure(figsize=(8, 6))
    venn3(selected_sets, set_labels=["Human Computer Interaction", "Computer Vision","Data Mining"])
    plt.title("Overlap of Top Central Researchers")
    plt.show()