import requests
import gzip
import networkx as nx
from io import BytesIO

# Step 1: download and load
url = "http://snap.stanford.edu/data/facebook_combined.txt.gz"
response = requests.get(url)
response.raise_for_status()

G = nx.read_edgelist(BytesIO(gzip.decompress(response.content)), nodetype=int)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Step 2: connectivity and LCC
print("Is connected?", nx.is_connected(G))

largest_cc = max(nx.connected_components(G), key=len)
LCC = G.subgraph(largest_cc).copy()

print("LCC nodes:", LCC.number_of_nodes())
print("LCC edges:", LCC.number_of_edges())

# Part 2: centrality
deg = nx.degree_centrality(LCC)
pr  = nx.pagerank(LCC)
btw = nx.betweenness_centrality(LCC, k=500, seed=42)

nx.set_node_attributes(LCC, deg, "degree_centrality")
nx.set_node_attributes(LCC, pr,  "pagerank")
nx.set_node_attributes(LCC, btw, "betweenness_centrality")

# Quick sanity check: top 5 nodes for each measure
for name, d in [("degree", deg), ("pagerank", pr), ("betweenness", btw)]:
    top = sorted(d.items(), key=lambda x: x[1], reverse=True)[:5]
    print(name, top)

nx.write_graphml(LCC, "facebook_centrality.graphml")
print("Exported facebook_centrality.graphml")

import pandas as pd

df = pd.DataFrame({"degree": deg, "pagerank": pr, "betweenness": btw})
ranks = df.rank(ascending=False, method="min").astype(int)
ranks.columns = ["degree_rank", "pagerank_rank", "betweenness_rank"]

print(ranks.loc[[107, 1684, 1912, 3437, 0]])