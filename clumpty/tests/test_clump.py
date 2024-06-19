from clumpty.clump import clump_graph, clump_graph_expensive
from networkx import balanced_tree, graph_atlas, graph_atlas_g
import matplotlib.pyplot as plt
import networkx as nx
import random
import pytest
import pandas as pd

def atlas():
    """Make a test set of graphs """
    GraphMatcher = nx.isomorphism.vf2userfunc.GraphMatcher
    Atlas = nx.graph_atlas_g()[500:600]  # 0, 1, 2 => no edges. 208 is last 6 node graph
    U = nx.Graph()  # graph for union of all graphs in atlas
    for G in Atlas:
        # check if connected
        if nx.number_connected_components(G) == 1:
            # check if isomorphic to a previous graph
            if not GraphMatcher(U, G).subgraph_is_isomorphic():
                U = nx.disjoint_union(U, G)
    return U

def viz(cg, G, num = 1):
    """
    from clumpty.clump import clump_graph, clump_graph_expensive
    cg_basic = clump_graph(nn, min_degree = 1)
    cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
    viz(cg_exp, num = 2)
    viz(cg_basic, num = 1)
    """
    import matplotlib.pyplot as plt
    from tcrdist.html_colors import get_html_colors
    colors = dict()
    html_colors = get_html_colors(len(cg.keys()))

    var_to_col = {k:v for k,v in zip(cg.keys(), html_colors)}

    for k,v in cg.items():
        print(v)
        for i in v:
            colors[i] = var_to_col.get(k)

    plt.figure(num, figsize=(8, 8))
    # layout graphs with positions using graphviz neato
    pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
    # color nodes the same in each connected subgraph
    C = (G.subgraph(c) for c in nx.connected_components(G))
    for g in C:
        c = [colors.get(i, "black") for i in g.nodes] # random color...
        nx.draw(g, pos, node_size=40, node_color=c, vmin=0.0, vmax=1.0, with_labels=False)

    print(f'test_clumping_{num}.pdf')
    plt.savefig(f'test_clumping_{num}.pdf')


# create test nn 
G = atlas()
# s = list()
# for i,j in G.edges:
#   s.append((i,j))
# df = pd.DataFrame(s, columns = ['i','j'])
# df.to_csv("clumpty/tests/nn.csv", index = False)

import pandas as pd
df = pd.read_csv("clumpty/tests/nn.csv")
edges = df.to_dict('split')['data']
nn = dict()
for i,j in edges:
    nn.setdefault(i,[]).append(j)
    nn.setdefault(j,[]).append(i)


def test_basic():
    cg_basic = clump_graph(nn, min_degree = 1)
    assert isinstance(cg_basic, dict)

def test_clump_graph_expensive():
    cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
    assert isinstance(cg_basic, dict)

@pytest.mark.skip(reason="Don't remake plots in random places")
def test_viz()
    from clumpty.clump import clump_graph, clump_graph_expensive
    cg_basic = clump_graph(nn, min_degree = 1)
    cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
    viz(cg_exp, num = 2)
    viz(cg_basic, num = 1)

    
