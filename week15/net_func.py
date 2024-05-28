import pandas as pd
import numpy as np
import pyvis
import networkx as nx
import IPython
import random
import re


def random_color():
  r = lambda: random.randint(0,255)
  return '#%02X%02X%02X' % (r(),r(),r())

def matPresentGraph(mat:np.array,node_id:list,node_type:list=None,node_value:list = None,directed = True,edge_color=None) -> pyvis.network.Network:

  if directed != True:
    if (mat == mat.transpose()).all():
      print('matrix is Symmetric')
    else:
      print('matrix is not Symmetric')
  if node_type == None:
    c = random_color()
    node_colors = [c for i in range(len(node_id))]
    node_type = [" " for i in range(len(node_id))]
  else:
    node_color_map = {}
    for i in set(node_type):
      while True:
        c = random_color()
        if c not in node_color_map.values():
          break
      node_color_map[i] = c
    node_colors = [node_color_map[i] for i in node_type]
  # print(node_colors)
  if edge_color == None:
    edge_color = random_color()
  edge_color = random_color()
  if node_value == None:
    node_value = [1 for i in range(len(node_id))]

  net = pyvis.network.Network(notebook=True, directed = directed, cdn_resources='in_line')
  
  titles_list = []
  for i ,j in zip(node_id,node_type):
    titles_list.append(str(i)+":"+str(j))

  net.add_nodes(
      nodes = node_id,
      value = node_value,
      label = node_id,
      title = titles_list,
      color = node_colors
  )

  for row in range(len(node_id)):
    for col in range(len(node_id)):
      if mat[row][col]>0.:
        net.add_edge(
            node_id[row],node_id[col],width = mat[row][col],color = edge_color,title = mat[row][col]
        )
  net.repulsion()
  return net


def centralityGraph(mat:np.array,alg:str,max_iter:int):
    sym = False
    if (mat == mat.transpose()).all():
        print('matrix is Symmetric')
        sym = True
    else:
        print('matrix is not Symmetric')
    alg_dict = {
        'eig':nx.eigenvector_centrality,
        'page':nx.pagerank,
        'hits':nx.hits,
        'betw':nx.betweenness_centrality
    }
    if alg in ['eig','betw']:
        if sym == False:
            tri = (np.tril(mat,-1).T + np.triu(mat,1))
            mat = tri+tri.T
        G = nx.Graph((mat))
        score = alg_dict[alg](G,max_iter=max_iter)
    elif alg == 'page':
        G = nx.DiGraph((mat))
        score = alg_dict[alg](G,max_iter=max_iter)
    elif alg =='hits':
        G = nx.DiGraph((mat))
        out_,in_ = alg_dict[alg](G,max_iter=max_iter)
    else:
        raise(f"No '{alg}' centrality")
    return list(score.values())
def getMeasure(mat:np.array):
    if (mat == mat.transpose()).all():
        pass
    else:
        tri = (np.tril(mat,-1).T + np.triu(mat,1))
        mat = tri+tri.T
    G = nx.Graph(mat)
    G_sub = sorted(nx.connected_components(G), key=len, reverse=True)
    G_max_sub = G.subgraph(G_sub[0])
    sub_mat = nx.adjacency_matrix(G_max_sub).todense()
    G = nx.Graph(sub_mat)

    return {
        "transitivity":nx.transitivity(G),
        "density":nx.density(G),
        "distance":nx.average_shortest_path_length(G),
        "diameter":nx.diameter(G),
        "clustering":nx.average_clustering(G)
    }



    