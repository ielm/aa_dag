"""
Test file for graph creation and visualization from HTN tree. As of this writing there is no error handling for incorrect input.

TODO:
  - add instance ID to each "duplicate" step (such as multiple calls to get-dowel or screw-in)
  - organize graph vizualization into vertical layers
  - Recolor nodes and add attributes
"""

import json
import pprint
# import pygraphviz as pgv
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import pydot as dot
from collections import Counter


import maketree
import mergetree
import ontosend
import tmrutils
from treenode import *

# No index or duplicates. Each action or utterance gets a single node in the graph.
def addNodes(tree, graph):
  if len(tree.name) == 0:
    graph.add_node("BASE")
  else:
    graph.add_node(tree.name)
  for child in tree.children:
    addNodes(child, graph)

def addEdges(tree,graph):
  for child in tree.children:
    if len(tree.name) == 0:
      tempname = "BASE"
    else:
      tempname = tree.name
    graph.add_edge(tempname, child.name)
    addEdges(child, graph)

# Assumes correct graph; no error handling...
def add_n_nodes(tree, graph, dups):
  if len(tree.name) == 0:
    print("tree name is null")
    graph.add_node("BASE")
  else:
    if tree.name not in dups:
      dups[tree.name] = 0
      graph.add_node(tree.name +'-'+str(dups[tree.name]))

    elif tree.name in dups:
      graph.add_node(tree.name+'-'+str(dups[tree.name]))
      dups[tree.name] += 1
    # print(tree.name) i
  for child in tree.children:
    add_n_nodes(child, graph, dups)
    # print(child.name)

def add_n_edges(tree, graph, dups):
  for child in tree.children:
    if len(tree.name) == 0:
      tempname = "BASE"
    else:
      if tree.name not in dups:
        tempname = tree.name + '-0'
      elif tree.name in dups:
        tempname = tree.name +'-'+str(dups[tree.name])
    graph.add_edge(tempname, child.name)
    add_n_edges(child, graph, dups)

def stack_layout(G, scale=1, height=1, width=1,center=None, dim=2):
  """
  Positions nodes in a stacked hierarchical grid

  Parameters
  ----------
  G : NetworkX graph or list of nodes
      A position will be assigned to every node in G

  height : number (default: 1)
      Height of each row

  width : number (default: 1)
      Width of each node

  scale : number (default: 1)
      Scale factor for positions

  dim : int
      Dimension of layout.
      If dim>2, the remaining dimensions are set to zero
      in the returned positions.

  Returns
  -------
  pos : dict
      A dictionary of positions keyed by node

  """

  import numpy as np

  G, center = nx.layout._process_params(G, center, dim)

  paddims = max(0, (dim - 2))

  if len(G) == 0:
    return {}
  elif len(G) == 1:
    return {nx.utils.arbitrary_element(G): center}
  # else:

# Graphviz add_nodes -> DO NOT USE, USE NX INSTEAD
def add_gv_nodes(tree, graph):
  if not type(tree) is TreeNode:
    print("not TreeNode")
    return
  if len(tree.name) == 0:
    print("none")
  else:
    graph.add_node(tree.name)
  for child in tree.children:
    add_gv_nodes(child, graph)
    # graph.add_edge(tree.name, child.name)
# Graphviz add_edges -> DO NOT USE, USE NX INSTEAD
def add_gv_edges(tree, graph):
  # cp = tree.name
  for child in tree.children:
    if len(tree.children) > 1:
      graph.add_edge(tree.name, child.name, color='blue')
      add_gv_edges(child, graph)

# def nomBuilder(json_tree):
#   tree = []
#   for i in json_tree:
#     graph = ""
#     graph += str(i["id"]) + ": " + i["name"] + " "
#     for child in i["children"]:
#       graph += '\n' + "  " + child
#     tree.append(graph)
#   return tree

# def nomBuilder(json_tree):
#   tree = dict()
#   for i in json_tree:
#     print(i["name"])
#     tree[i["name"]] = []
#     for child in i["children"]:
#       print(" " + child)
#       tree[i["name"]].append(child)
#   return tree

def nodeBuilder(json_tree):
  graph = []
  parents = []
  for i in json_tree:
    node_group = []
    node_group.append(i["name"])
    parents.append(i["name"])
    children = []
    for child in i["children"]:
      children.append(child)
    node_group.append(children)
    graph.append(node_group)
  parents = Counter(parents)


  return graph, parents

def nomBuilder(nodes):
  graph = ""
  seen = []
  # counts = []
  for node in nodes:
    # print(node[0])
    seen.append(node[0])
    base = "[" + node[0] + "-" + str(seen.count(node[0])-1) + "]"
    children = []
    for child in node[1]:
      if child.isupper():
        children.append(child)
      # print("[" + node[0] + "-" + str(seen.count(node[0]) - 1) + "]" + "-> " + "[" + child + "]")
      # print("-" + child)
      line = base + " -> "
      c_line = ""
      # if child.islower():





if __name__ == '__main__':
  data = json.load(open('test/actions_sem.json'))

  s = []
  Tree = maketree.construct_tree(data, s)
  # maketree.print_tree(Tree, "- ")
  # print("\nNumber of steps: " + str(len(s)))

  # pp = pprint.PrettyPrinter(indent=2)

  json_list = []

  maketree.tree_to_json_format(Tree, json_list)

  # pp.pprint(json_list)


  nodes, parents = nodeBuilder(json_list)
  nomBuilder(nodes)


  print(parents)

  # print(s)
  # for i in s:
  #   # print(i[])
  #   print('\n------------------------------------------')
  #   print('Input')
  #   print(i['input'])
  #   print("\nTree")
  #   print(i['tree'])

### Networkx Graph Init
  # nxG = nx.DiGraph()
  # nxG = nx.Graph()

  # NodeDups = {}
  # EdgeDups = {}
### BUILD GRAPH
  # add_n_nodes(Tree, nxG, NodeDups)
  # add_n_edges(Tree, nxG, EdgeDups)

  # addNodes(Tree, nxG)
  # addEdges(Tree, nxG)

  # pos = nx.nx_agraph.graphviz_layout(nxG)

  # pos = nx.circular_layout(nxG)
  # pos = nx.kamada_kawai_layout(nxG)

  # print(pos)
### DRAW GRAPH
  # nx.draw(nxG, with_labels=True, pos=pos)
  # nx.draw_shell(nxG, with_labels=True)
  # nx.draw_networkx(nxG, with_labels=True)
  # nx.draw_kamada_kawai(nxG, with_labels=True)
  # nx.draw_spring(nxG, with_labels=True)
  # nx.draw_spectral(nxG, with_labels=True)i

  # A = nx.nx_agraph.to_agraph(nxG)

### nx to DOT
  # nx.nx_agraph.to_agraph(nxG)
  # nx.nx_pydot.graphviz_layout(nxG)

### SHOW GRAPH
  # plt.savefig("fig1.png")
  # write_dot(nxG, 'file.dot')
  # plt.show()

# GRAPHVIZ
  # G = pgv.AGraph(directed=True)
  # add_gv_nodes(Tree, G)
  # add_gv_edges(Tree, G)
  # s = G.string()
  # print(s)
  # # specify prog=neato|dot|twopi|circo|fdp|nop.
  # G.layout(prog='dot')
  # G.draw("file2.png")



