import os 
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def getPackageNameAndDependencies(path):
    with open(os.path.join(path, "package.json")) as f:
        packageFile = json.load(f)

    packageName = packageFile["name"]
    dependencies = packageFile["dependencies"]
    return packageName, dependencies

def joinDependencyVersion(dependencyList):
    dep = []
    for k in dependencyList.keys():
        dep.append(k+'@'+dependencyList[k])
    return dep

path = "D:/Updated Repository/imodeljs-core/core/backend/"


nodes = []
packageName, dependencies = getPackageNameAndDependencies(path)
dependencies = joinDependencyVersion(dependencies)

G = nx.DiGraph()
G.add_node(packageName)
G.add_nodes_from(dependencies)

for d in dependencies:
    G.add_edges_from([(packageName, d)])

figure(num=None, figsize=(10, 10), dpi=150, facecolor='w', edgecolor='k')
nx.draw_circular(G, with_labels=True)
plt.savefig('dependency_graph.png')