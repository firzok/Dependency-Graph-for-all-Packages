#--------------------------------------------------------------------------------------
#
#     $Source: CommonTasks/dependency_graph.py $
#
#  $Copyright: (c) 2018 Bentley Systems, Incorporated. All rights reserved. $
#
#--------------------------------------------------------------------------------------
import os
import json
import argparse
import numpy as np
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
from collections import OrderedDict
# Generates a dependency graph based on a package-lock.json file


#-------------------------------------------------------------------------------------------
# bsimethod                                     Firzok.Nadeem                    07/2018
#-------------------------------------------------------------------------------------------
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



#---Entry point of the Script ---#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('packageLockPath', help="Path to the package-lock.json file.")
    args = parser.parse_args()


    packageLockPath = args.packageLockPath

    with open(packageLockPath) as f:
            packageLockFile = json.load(f)

    dependencies = json.load(open(packageLockPath), object_pairs_hook=OrderedDict)['dependencies']
    packageName = list(dependencies.keys())[0]
    fileName = 'dependency_graph_'+packageLockFile['name']+'.png'

    nodeName = packageName+'@'+dependencies[packageName]['version']

    G = nx.DiGraph()
    q = deque([list(dependencies.keys())[0]])
    makeGraph(q, G)

    plt.figure(num=None, figsize=(20, 20), dpi=150, facecolor='w', edgecolor='k')
    pos = nx.circular_layout(G, scale=2)

    pos[nodeName] = [0, 0]  #Places the parent node in the middle

    nx.draw_networkx(G, pos, with_labels=True, arrowstyle = 'simple', arrowsize = 10, node_size = 700,
                node_color=np.arange(0, len(G.nodes())), node_shape = 'h', alpha = 1,
                edge_color = 'green', font_color ='red', scale = 15, font_weight = 'heavy')

    fileName = fileName.replace('/','_')
    plt.savefig(fileName)