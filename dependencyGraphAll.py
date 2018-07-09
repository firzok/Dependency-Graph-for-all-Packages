import os
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def getDependencies():
    path = "D:/Updated Repository/imodeljs-core/"
    with open(os.path.join(path, "rush.json")) as f:
        rushFile = json.load(f)

    packages = rushFile["projects"]

    paths = []
    packageName = []
    for package in packages:
        packageName.append(package["packageName"])
        paths.append(os.path.join(os.getcwd(), package["projectFolder"]))

    d = dict()
    packageNames = []
    dependencies = []
    for path in paths:
        with open(os.path.join(path, "package.json")) as f:
            fileData = json.load(f)
            packageNames.append(fileData["name"])
            dependencies.append(fileData["dependencies"])
            d[fileData["name"]] = fileData["dependencies"]
    return d


def joinDependencyVersion(dependencyList):
    dep = []
    for k in dependencyList.keys():
        dep.append(k+'@'+dependencyList[k])
    return dep


nodes = []
d = getDependencies()
dependencies = dict()
for x in d.items():
    dependencies[x[0]] = joinDependencyVersion(x[1])
    nodes.append(x[0])
    nodes.extend(dependencies[x[0]])


G = nx.DiGraph()
G.add_nodes_from(nodes)


for d in dependencies.items():
    for x in d[1]:
        G.add_edges_from([(d[0], x)])

plt.figure(num=None, figsize=(20, 20), dpi=150, facecolor='w', edgecolor='k')
nx.draw_circular(G, with_labels=True)
plt.savefig('dependency_graph.png')
