import networkx as nx
import matplotlib.pyplot as plt
from string import ascii_uppercase
import random

# Generer unikke node ID'er
def generate_node_id(n):
    return [
        #modulus 26 for at få bogstaverne til at gentage sig og der er 26 bogstaver i engelsk alfabetet
        ascii_uppercase[i % 26] + 
        # +1 for at få tal til at starte fra 1 og ikke 0
        str(i + 1) 
        for i in range(n)
    ]

# Generer en komplet graf med vægte
def generate_complete_graph(nodes):
    edges = []
    weights = {}
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            edge = (nodes[i], nodes[j])
            weight = random.randint(1, 10)  # Tilfældigt vægt
            edges.append(edge)
            weights[edge] = weight
    return edges, weights

# Grådig algoritme for TSP
def greedy_tsp(nodes, weights):
    visited = {node: False for node in nodes}

    current_node = nodes[0]
    path = [ current_node ]
    total_cost = 0

    # Vi vil besøge alle noder i grafen så derfor tjekker vi om slut ruten er lige så lang 
    # Eller længere end noderne 
    while len(path) < len(nodes):
        visited[current_node] = True
        next_node = None
        min_cost = float('inf')
        for neighbor in nodes:
            # Tjek om kanten findes i grafen, og om den er mindre end den nuværende
            # vi gør det 2 gange for at være sikker på at vi får den rigtige vægt, da den kan ligge som -
            # (w, v) eller (v, w)
            
            if not visited[neighbor] and (current_node, neighbor) in weights:
                cost = weights[(current_node, neighbor)]
                if cost < min_cost:
                    next_node = neighbor
                    min_cost = cost

            elif not visited[neighbor] and (neighbor, current_node) in weights:
                cost = weights[(neighbor, current_node)]
                if cost < min_cost:
                    next_node = neighbor
                    min_cost = cost

        #hvis der ikke er en næste node, så er kredsen ikke lukket og derfor -
        #kan vi ikke finde en hamilton kreds
        if next_node is None:
            print("Hamilton-kreds ikke mulig.")
            return


        path.append(next_node)
        total_cost += min_cost
        current_node = next_node

    # Tilføj sidste kant til ruten som også skal være der fordi eller er det ikke en hamilton kreds
    final_edge = (current_node, path[0]) if (current_node, path[0]) in weights else (path[0], current_node)
    # Tjek om kanten findes i grafen
    if final_edge in weights:
        total_cost += weights[final_edge]
        path.append(path[0])
        print("Grådig TSP-løsning:", path)
        print("Total omkostning:", total_cost)
    else:
        print("Hamilton-kreds ikke mulig.")


nodes = generate_node_id(5)
edges, weights = generate_complete_graph(nodes)
greedy_tsp(nodes, weights)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos = nx.spring_layout(G)  
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, label_pos=0.5, font_size=8)

plt.show()