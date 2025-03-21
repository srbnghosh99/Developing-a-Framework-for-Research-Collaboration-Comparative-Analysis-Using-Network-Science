import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Generate a 4x4 matrix with random values (Replace this with actual data if needed)
data = np.random.rand(4, 4)

# Define labels for rows and columns (Optional: Use actual domain names if relevant)
labels = ["Uni-RC", "Uni-Com", "Com-RC", "Uni-Company Relab"]

# Create the heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(data, annot=True, cmap="crest", xticklabels=labels, yticklabels=labels, linewidths=0.5)
# sns.heatmap(glue, annot=glue.rank(axis="columns"))
plt.yticks(rotation=45)
plt.title("Collaboration between Different Affiliations ")
plt.tight_layout()
plt.show()
