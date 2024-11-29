from os import system; system('cls') # Fjerner alt i konsollen, mest brugt til at debug i terminalen

import networkx as nx
import matplotlib.pyplot as plt
from string import ascii_uppercase
import random

# Til at navne til noder
last_node_id = 0
last_node_char_id = 'A'

def generate_node_id():
    global last_node_id

    tmp_node_id = last_node_id % 26
    last_node_id += 1

    return str(ascii_uppercase[tmp_node_id] + str( (tmp_node_id) + 1 ))

def generate_nodes(n=10):
    nodes = []
    for i in range(n):
        nodes.append(generate_node_id())
    return nodes

def generate_edges(nodes=[], n=10):
    edges = []

    for i in range(len(nodes) - 1):
        edges.append((nodes[i], nodes[i + 1]))

    while len(edges) < n:
        # Tager 2 noder tilfældigt fra listen
        u, v = random.sample(nodes, 2)

        # laver en edge med de punkter
        edge = (u, v)

        # Vi tjekker for at se om vi allerede har den edge så vi ikke lave de to samme edges
        if edge not in edges and (v, u) not in edges and (u, v) not in edges and (u != v) :
            edges.append(edge)

    return edges


def generate_weights(edges):
    weights = {}
    for edge in edges:
        weights[edge] = random.randint(1, 10) 
    return weights

# G = (V, E) 
P = nx.Graph()
nodes = generate_nodes(20)
edges = generate_edges(nodes, 30)
weights = generate_weights(edges)

def sort(l):
    l.sort(key = lambda node: node["weigth"])


def get_edge_weight(edge):
    if edge in weights:
        return weights[edge]
    elif (edge[1], edge[0]) in weights:
        return weights[(edge[1], edge[0])]

def get_node(nodes, node_name):
    for node in nodes:
        if node["node"] == node_name:
            return node
    return None


def get_node_neighbours(node, edges):
    neighbours = []

    for edge in edges:
        if edge[0] == node:
            neighbours.append(edge[1])
        
        elif edge[1] == node:
            neighbours.append(edge[0])
    
    return neighbours


def djikstra_algo(start, target, nodes, edges):
    nodes = [{"node": node, "weigth": float('inf'), "path": None} for node in nodes]
    has_visited = []
    
    # sætter start nodesne til 0 for den ikke medregner den i vægten, det er i bund og grund lidt ubrugeligt men hvis vi vil se 
    # vægten fra start til start ordenligt så det bedste at sætte det til 0
    start_node = get_node(nodes, start)
    if start_node:
        start_node["weigth"] = 0
    
    while len(has_visited) < len(nodes):
        sort(nodes)  # Sorterer noderne efter vægt så queuen er i den rigtige rækkefølge
        current_node = nodes.pop(0) # Fjerner den første node i listen
        
        if current_node in has_visited: # Hvis vi allerede har besøgt noden, så fortsæt. Selvom det ikke rigtig burde kunne ske.
            continue

        has_visited.append(current_node) # Tilføjer noden til listen over besøgte noder

        # Hvis vi så når til target så har vi klaret det og breaker ud af loopet    
        # Jeg er lidt usikker på om den vælger den mest optimiseret rute eller bare den første rute den kan få, men stadig med alle dens tjeks om længde osv.


        if current_node["node"] == target:
            print("breaking")
            break

        # Henter naboer til noden og looper gennem alle edges til naboen
        neighbours = get_node_neighbours(current_node["node"], edges)

        for neighbour in neighbours:
            # Henter nabo noden

            neighbour_node = get_node(nodes, neighbour)

            # Hvis naboen ikke er besøgt og ikke er None
            if neighbour_node and neighbour_node not in has_visited:

                # laver en temporary edge fir at finde vægten og sammenligne
                edge = (current_node["node"], neighbour)
                new_weight = current_node["weigth"] + get_edge_weight(edge)
                
                # Updatere vægten hvis at vægten er mindre end den nuværende vægt
                if new_weight < neighbour_node["weigth"]:
                    neighbour_node["weigth"] = new_weight
                    neighbour_node["path"] = current_node["node"]

    print(nodes)
    


    path = []
    node = get_node(nodes + has_visited, target)
    print(node)
    while node and node["node"] != start:
        
        path.append(node["node"])
        node = get_node(nodes + has_visited, node["path"])

    path.append(start)
    path.reverse()

    print("Shortest path:", path)
    print("Target weight:", get_node(nodes + has_visited, target)["weigth"])


        
        
    







    





djikstra_algo("A1", "T20", nodes, edges)



P.add_nodes_from(nodes)
P.add_edges_from(edges)

#print(P.nodes())
#print(P.edges())

pos = nx.spring_layout(P)  # Layout for nodes
nx.draw(P, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=10)

nx.draw_networkx_edge_labels(P, pos, edge_labels=weights, label_pos=0.5, font_size=8)

plt.show()
 