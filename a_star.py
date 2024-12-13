from os import system; system('cls') # Fjerner alt i konsollen, mest brugt til at debug i terminalen

from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt
from string import ascii_uppercase
import random

# Til at tildele navne til knuderne
last_node_id = 0
last_node_char_id = 'A'

# Generer en unik knude ID
def generate_node_id():
    global last_node_id

    tmp_node_id = last_node_id % 26
    last_node_id += 1

    return str(
        ascii_uppercase[tmp_node_id] +  # Vi bruger modulus 26 for at få bogstaverne til at gentage sig
        str( (tmp_node_id) + 1 ) # +1 for at få tal til at starte fra 1 og ikke 0
    )

# Generer n knuder
def generate_nodes(n=10):
    nodes = []
    for i in range(n): # Vi generere n knuder
        nodes.append(generate_node_id())
    return nodes

# Generer kanter for en liste af knuder
def generate_edges(nodes=[], n=10):
    edges = []

    # Vi laver en kant mellem hver knude i listen
    for i in range(len(nodes) - 1):
        edges.append((nodes[i], nodes[i + 1]))

    # Vi laver n kanter i alt for at få en mere tæt graf
    while len(edges) < n:
        # Tager 2 noder tilfældigt fra listen
        u, v = random.sample(nodes, 2)

        # laver en edge med de punkter
        edge = (u, v)

        # Vi tjekker for at se om vi allerede har den edge så vi ikke lave de to samme edges
        if edge not in edges and (v, u) not in edges and (u, v) not in edges and (u != v) :
            edges.append(edge)

    return edges

# Generer vægte for en liste af kanter
def generate_weights(edges):
    weights = {}
    for edge in edges: # Vi generere en vægt for hver kant
        weights[edge] = random.randint(1, 10) 
    return weights


# G = (V, E) 
P = nx.Graph()
nodes = generate_nodes(20)
edges = generate_edges(nodes, 30)
weights = generate_weights(edges)


# Find en vægt for en kant og vi gør det begge veje in case at vægten ligger som (w, v) eller (v, w)
def get_edge_weight(edge): 
    if edge in weights:
        return weights[edge]
    elif (edge[1], edge[0]) in weights:
        return weights[(edge[1], edge[0])]

# Find en node i en liste af knuder
def get_node(nodes, node_name):
    for node in nodes:
        if node["node"] == node_name:
            return node
    return None

# Find naboer til en knude
def get_node_neighbours(node, edges):
    neighbours = []

    for edge in edges:
        if edge[0] == node:
            neighbours.append(edge[1])
        
        elif edge[1] == node:
            neighbours.append(edge[0])
    
    return neighbours



# Herustic delen til A* algoritmen, det er lidt dårligt brugt i dette tilfælde da grafen vi bruger ikke har position men det er -
# vores netværks visualisering der sætter noderne tilfældigt så vi tager bare og laver herustik efter tallet efter bogstavet for at demonstrere det
def heuristic(node, target):
    node_index = int(node[1:])  # tager tallet fra noden, f.eks. "A1" -> 1
    target_index = int(target[1:])  # -||-
    return abs(node_index - target_index) # returnere den absolutte værdi af forskellen mellem de to tal


def a_star_algo(start, target, nodes, edges):
    # Denne algoritme har vi brugt en kø (PriorityQueue) til at holde styr på hvilke knuder vi skal besøge næste gang
    # Det medfører at tids kompleksiteten er O(e+v log v) i stedet for O(v^2) som vi ville have hvis vi brugte en simpel list som vi feks gjorde i djikstra

    open_set = PriorityQueue()
    open_set.put((0, start))  # Køen bliver (h_score, node)

    came_from = {} # Holder styr på hvilken node vi kom fra
    
    # Vores g_score og h_score er sat til uendelig for alle knuder
    # g_score er vægten uden herustik
    # h_score er vægten med herustik

    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    h_score = {node: float('inf') for node in nodes}
    h_score[start] = heuristic(start, target)

    # Vi bruger en set til at holde styr på hvilke knuder vi har besøgt
    closed_set = set()

    # Vi kører så længe der er knuder i køen
    while not open_set.empty():
        _, current = open_set.get() # Vi tager den knude med den laveste h_score

        if current in closed_set: # Hvis vi allerede har besøgt knuden så springer vi over
            continue
        closed_set.add(current) # Vi tilføjer knuden til vores besøgte knuder

        if current == target: # Hvis vi har fundet target knuden så bryder vi ud af løkken
            path = [] # Vi laver en liste over den korteste veg og går baglæns igennem 
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse() # Vi har gået baglæns, så vi skal vende listen om for at få stien

            print("Shortest path:", path)
            print("Target weight:", g_score[target])

            return path, g_score[target]

        neighbors = get_node_neighbours(current, edges) # Vi finder naboer til den nuværende knude
        for neighbor in neighbors: # Vi går igennem alle naboer til knuden
            temp_g_score = g_score[current] + get_edge_weight((current, neighbor)) # Vi finder vægten for kanten
            
            if temp_g_score < g_score[neighbor]: # Hvis den nye vægt er mindre end den gamle vægt
                came_from[neighbor] = current # Sæt den nuværende knude som den forrige knude
                g_score[neighbor] = temp_g_score # Vi opdaterer g_score
                h_score[neighbor] = temp_g_score + heuristic(neighbor, target) # Vi opdaterer h_score
                open_set.put((h_score[neighbor], neighbor)) # Vi tilføjer knuden til køen
    
    return None, float('inf')



P.add_nodes_from(nodes)
P.add_edges_from(edges)

pos = nx.spring_layout(P)
path, cost = a_star_algo("A1", "T20", nodes, edges)
if path:
    path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    edge_colors = ["red" if edge in path_edges or (edge[1], edge[0]) in path_edges else "black" for edge in P.edges]
    nx.draw(P, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(P, pos, edge_labels=weights, label_pos=0.5, font_size=8)
    plt.show()

else:
    print("No path found")