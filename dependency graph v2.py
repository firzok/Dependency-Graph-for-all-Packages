import os 
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

packageLockPath = input("Enter the package-lock.json path:\n")

with open(packageLockPath) as f:
        packageLockFile = json.load(f)

dependencies = packageLockFile['dependencies']
packageName = list(dependencies.keys())[0]
fileName = 'dependency_graph_'+packageLockFile['name']+'.png'

nodeName = packageName+'@'+dependencies[packageName]['version']
def makeGraph(queue, graph):
    if (len(queue)) == 0:
        return
    n = queue.popleft()
    node = n+'@'+dependencies[n]['version']
    graph.add_node(node)

    if dependencies[n].get('requires'):
        
        for i in dependencies[n]["requires"]:
#             graph.add_edges_from([(node,i+'@'+dependencies[n]["requires"][i])])
            graph.add_edges_from([(node,i+'@'+dependencies[i]["version"])])
            queue.append(i)
    makeGraph(queue, graph)

G = nx.DiGraph()
q = deque([list(dependencies.keys())[0]])
makeGraph(q, G)

plt.figure(num=None, figsize=(20, 20), dpi=150, facecolor='w', edgecolor='k')
pos = nx.circular_layout(G, scale=2)

# pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)

pos[nodeName] = [0, 0]


nx.draw_networkx(G, pos, with_labels=True, arrowstyle = 'simple', arrowsize = 10, node_size = 700,
               node_color=np.arange(0, len(G.nodes())), node_shape = 'h', alpha = 1,
              edge_color = 'green', font_color ='red', scale = 15, font_weight = 'heavy')

plt.savefig(fileName)