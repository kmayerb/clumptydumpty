# simple 
import networkx as nx
import sys
sys.path.append('/fh/fast/gilbert_p/kmayerbl/gitfix/clumpty/')
from clumpty.clump import clump_graph, recompute_nn, clump_graph_expensive, clump_graph_expensive_by_component_parmap
#print(sys.path)
def atlas():
    """Make a test set of graphs """
    GraphMatcher = nx.isomorphism.vf2userfunc.GraphMatcher
    Atlas = nx.graph_atlas_g()[900:1020]  # 0, 1, 2 => no edges. 208 is last 6 node graph
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

#G = atlas()

def test_parmap_version_for_efficiency():
    import networkx as nx
    from clumpty.clump import clump_graph_expensive_by_component_parmap
    G1 = nx.balanced_tree(r=2, h=4)
    G2 = nx.balanced_tree(r=2, h=5)
    G3 = nx.balanced_tree(r=2, h=2)
    U = nx.disjoint_union(G1, G2)
    U = nx.disjoint_union(U,G3)

    cg_exp1 = clump_graph_expensive_by_component_parmap(U, cpus = 2)
    viz(cg_exp1, U, 3)

    # slow version
    cg_all = list()
    S = [U.subgraph(c).copy() for c in nx.connected_components(U)]
    for g in S:
        nn = dict()
        for i,j in g.edges:
            nn.setdefault(i,[]).append(j)
            nn.setdefault(j,[]).append(i)
        cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
        cg_all.append(cg_exp)
    cg_exp2 = dict()
    for d in cg_all:
        cg_exp2.update(d)

    assert cg_exp1 == cg_exp2


def test_clump_components_with_network_x_parmap():
    import networkx as nx
    from clumpty.clump import clump_components_with_networkx_parmap
    G1 = nx.balanced_tree(r=2, h=4)
    G2 = nx.balanced_tree(r=2, h=5)
    G3 = nx.balanced_tree(r=2, h=2)
    U = nx.disjoint_union(G1, G2)
    U = nx.disjoint_union(U,G3)
    cg_exp = clump_components_with_networkx_parmap(G=U.copy(), cpus = 2)
    viz(cg_exp, U, num = 7)
    assert isinstance(cg_exp, dict)



# import networkx as nx
# from clumpty.clump import clump_graph_expensive_by_component_parmap
# G1 = nx.balanced_tree(r=2, h=4)
# G2 = nx.balanced_tree(r=2, h=5)
# G3 = nx.balanced_tree(r=2, h=2)
# U = nx.disjoint_union(G1, G2)
# U = nx.disjoint_union(U,G3)
# degrees = list(U.degree())
# print(sum([x[1] for x in degrees]))
# # Sort by degree, descending
# degrees_sorted_by_degree = sorted(degrees, key=lambda x: x[1], reverse=True)
# node = degrees_sorted_by_degree[0][0]
# U.remove_node(1)
# degrees = list(U.degree())
# print(sum([x[1] for x in degrees]))
# # Sort by degree, descending
# degrees_sorted_by_degree = sorted(degrees, key=lambda x: x[1], reverse=True)




# test_parmap_version_for_efficiency()


