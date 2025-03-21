import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import powerlaw
import seaborn as sns

# Load your DataFrame (Assuming df has 'betweenness' and 'pagerank' columns)
# df = pd.read_csv("your_data.csv")  # Uncomment if loading from a file

# Extract values
df1 = pd.read_csv('centrality/centrality_sw.csv')
df2 = pd.read_csv('centrality/centrality_hri.csv')
df3 = pd.read_csv('centrality/centrality_dm.csv')
df4 = pd.read_csv('centrality/centrality_cv.csv')
# betweenness_values = df["betweenness"].values
# pagerank_values = df["Pagerank"].values


domains = {
    "Software Engineering": df1["betweenness"].values,
    "Robotics": df2["betweenness"].values,
    "Data Mining": df3["betweenness"].values,
    "Computer Vision": df4["betweenness"].values,
}

# Set colors for each domain
colors = ["blue", "red", "green", "purple"]
# colors = ["blue", "red","green"]
plt.figure(figsize=(8, 6))

for (domain, values), color in zip(domains.items(), colors):
    values = np.sort(values)[::-1]  # Sort in descending order
    ranks = np.arange(1, len(values) + 1)

    plt.scatter(values, ranks, color=color, alpha=0.7, label=domain)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Betweenness Centrality")
plt.ylabel("Rank")
plt.title("Log-Log Betweenness Centrality Comparison Across Domains")
plt.legend()
plt.show()



# Combine data into a single DataFrame for violin plot
df1["domain"] = "Software Engineering"
df2["domain"] = "Robtics"
df3["domain"] = "Data Mining"
df4["domain"] = "Computer Vision"

df_combined = pd.concat([df1, df2, df3,df4])
print(df_combined)
# Violin plot to show betweenness distribution
plt.figure(figsize=(8, 6))
sns.violinplot(x="domain", y="Pagerank", data=df_combined, inner="quartile", palette="Set2")
plt.xlabel("Domain")
plt.ylabel("Betweenness Centrality")
plt.title("Betweenness Centrality Distribution Across Domains")
plt.show()

