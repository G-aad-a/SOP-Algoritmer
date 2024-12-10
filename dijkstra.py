from os import system; system('cls') # Fjerner alt i konsollen, mest brugt til at debug i terminalen

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

nodes = generate_nodes(20) # Generere 20 noder
edges = generate_edges(nodes, 30) # Generere 30 kanter for de 20 kanters
weights = generate_weights(edges)

# Halv skidt sortering af knuderne,
# Jeg bruger kun denne funktion en gang som om man ikke bare kunne sætte den direkte ind hvor man brugte den?
# En ordenlig prioriterings kø ville være bedre
def sort(l):
    l.sort(key = lambda node: node["weigth"]) # Sortere listen efter vægt


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

# Djikstra algoritme til at finde den korteste vej fra start til target
def djikstra_algo(start, target, nodes, edges):
    original_nodes = nodes[:]  # Lav en kopi af knuderne for at undgå at fjerne dem helt
    nodes = [{
        "node": node, 
        "weigth": float('inf'), 
        "path": None
    } for node in nodes]
    has_visited = [] # En liste over knuder vi har besøgt
    
    start_node = get_node(nodes, start) # Find start knuden
    if start_node:
        start_node["weigth"] = 0 # Sæt vægten til 0 for start knuden for ellers vil den ikke blive valgt som den første knude
    
    while len(has_visited) < len(original_nodes):  # Brug original_nodes til at tælle, ikke nodes variablen
        sort(nodes)  # Sorterer knuderne efter vægt
        if not nodes:  # Hvis listen er tom, bryd ud af loopet
            break
        
        current_node = nodes.pop(0)  # Fjerner den første knude i listen
        if current_node in has_visited:  # Hvis vi allerede har besøgt knuden, så fortsæt
            continue

        has_visited.append(current_node)  # Tilføjer knuden til listen over besøgte knuder

        if current_node["node"] == target: # Hvis vi har fundet target knuden, så bryd ud af løkken
            break

        neighbours = get_node_neighbours(current_node["node"], edges)

        for neighbour in neighbours: # Gå igennem alle naboer til knuden
            neighbour_node = get_node(nodes, neighbour)

            if neighbour_node and neighbour_node not in has_visited: # Hvis nabo knuden ikke er besøgt og faktisk eksisterer
                edge = (current_node["node"], neighbour)
                new_weight = current_node["weigth"] + get_edge_weight(edge) # Find vægten for kanten
                
                if new_weight < neighbour_node["weigth"]: # Hvis den nye vægt er mindre end den gamle vægt
                    # Sæt den nye vægt og stien til den nuværende knude
                    neighbour_node["weigth"] = new_weight
                    neighbour_node["path"] = current_node["node"]

    path = [] # løsnings stien fra start til target
    node = get_node(nodes + has_visited, target) # laver nodes + has_visited, in case at alle fra knuderne ikke er blevet gennemgået før vi har fundet målet

    while node and node["node"] != start: # Vi vil gerne have stien fra start til target, så vi skal gå baglæns
        path.append(node["node"])
        node = get_node(nodes + has_visited, node["path"])

    path.append(start)
    path.reverse() # Vi har gået baglæns, så vi skal vende listen om for at få stien

    return path, get_node(nodes + has_visited, target)["weigth"]

        



P.add_nodes_from(nodes)
P.add_edges_from(edges)

pos = nx.spring_layout(P)  # Generer layout efter at have tilføjet alle noder og kanter

path, cost = djikstra_algo("A1", "T20", nodes, edges)

path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)] # får alle kanterne i løsningen
edge_colors = ["red" if edge in path_edges or (edge[1], edge[0]) in path_edges else "black" for edge in P.edges] # farver den rød hvis det er en del af løsnings stien hvis ikke så sort
nx.draw(P, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10, edge_color=edge_colors)
nx.draw_networkx_edge_labels(P, pos, edge_labels=weights, label_pos=0.5, font_size=8)
plt.show() # Viser grafen