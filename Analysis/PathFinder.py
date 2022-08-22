#finds shortest paths between topics

import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

x = 1000
conn = sqlite3.connect('wiki_1000_conn.db')
cursor = conn.cursor()
cursor.execute("SELECT topic FROM links where id < ?",(x,))
rows = cursor.fetchall()

for row in rows:
    G.add_node(row[0].replace("Wikipedia: ", ""))

for i in range(1, x):
    # Startknoten
    cursor.execute("SELECT conn FROM conn where id = ?", (i,))
    connetcions = cursor.fetchone()
    conns = str(connetcions)
    c = conns.replace("('", "").replace("')", "").replace("_", " ").split("/wiki/")

    nodes = list(G.nodes)
    for conn in c:
        if conn in nodes and not conn == nodes[i-1]:
            G.add_edge(nodes[i - 1], conn)

to_be_removed = [x for x in G.nodes() if G.degree(x) <= 1]

for x in to_be_removed:
    G.remove_node(x)

start = input("Start: ")
destination = input("Destination: ")
print(nx.shortest_path(G, start, destination))
