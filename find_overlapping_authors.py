import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import networkx as nx

# Example authors for each graph (you can replace these with your actual data)
G1 = nx.read_graphml('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/dblp_dm_filtered_22.graphml')

G2 = nx.read_graphml('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/dblp_sw_filtered_22.graphml')

G3 = nx.read_graphml('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/dblp_cv_filtered_22.graphml')

G4 = nx.read_graphml('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/csvfiles/dblp_hri_filtered_22.graphml')

authors_G1 = G1.nodes()
authors_G2 = G2.nodes()
authors_G3 = G3.nodes()
authors_G4 = G4.nodes()

# Create a Venn diagram for four sets
fig, axes = plt.subplots(2, 2, figsize=(12, 10))



venn3([authors_G1, authors_G2, authors_G3], 
      set_labels=('Data Mining', 'Software Engg', 'Computer Vision'),
      set_colors=('red', 'blue', 'green'), ax=axes[0, 0])

venn3([authors_G1, authors_G2, authors_G4], 
      set_labels=('Data Mining', 'Software Engg', 'Human Robot Interaction'),
      set_colors=('red', 'blue', 'yellow'), ax=axes[0, 1])

venn3([authors_G2, authors_G4, authors_G3], 
      set_labels=('Software Engg','Human Robot Interaction','Computer Vision'),
      set_colors=('blue', 'yellow', 'green'), ax=axes[1, 0])

venn3([authors_G1, authors_G4, authors_G3],  # Fixed last plot (previous duplicate)
      set_labels=('Data Mining','Human Robot Interaction','Computer Vision'),
      set_colors=('red', 'yellow', 'green'), ax=axes[1, 1])

plt.suptitle('Venn Diagram of Common Authors Across Four Graphs', fontsize=14)
for i, label in enumerate(['(a)', '(b)', '(c)', '(d)']):
    axes[i//2, i%2].set_title(label, loc='center', fontsize=12)

# plt.title('Venn Diagram of Common Authors Across Four Graphs')
plt.tight_layout()
plt.savefig('/Users/shrabanighosh/UNCC/Spring 2025/plos complex/fig/overlap.png')
plt.show()


# Show plot

# plt.show()
