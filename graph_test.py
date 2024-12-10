import networkx as nx
import matplotlib.pyplot as plt

# Opret en graf med træ-struktur
G = nx.Graph()

# Tilføj noder
nodes = ['v', 'w', 'u']
G.add_nodes_from(nodes)

# Tilføj kanter
edges = [('v', 'w'), ('w', 'u')]
G.add_edges_from(edges)

# Layout for træ-struktur
pos = nx.spring_layout(G)  # Eller nx.shell_layout for en anderledes præsentation

# Tegn grafen
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10, edge_color="black")
plt.show()