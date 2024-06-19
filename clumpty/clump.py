
def clump_graph(nn, min_degree = 1):
    """
    Clumping algorithm:
    1: Rank nodes by degree.
    2: For the node with highest degree, remove all 1st degree neighbors to form a clump
    3: For the next highest ranking node take all remaining neighbors form the next clump
    """
    nodes = {x:1 for x in nn.keys()}
    knn = {k:len(v) for k,v in nn.items() if len(v) > 2}
    knn = dict(sorted(knn.items(), key=lambda item: item[1],reverse = True))
    clumps = dict()
    for node, degree in knn.items():
        if nodes.get(node) == 1:
            xs = nn[node]
            xs = [x for x in xs if nodes.get(x) == 1] + [node]
            if len(xs) > min_degree:
                clumps[node] = xs
                for x in xs:
                    nodes[x] = 0
    return clumps
    
def recompute_nn(nn, all_nodes):
    """
    Parameters
    ----------
    nn : dictionary of list (with neighbor indices)
    all_nodes : dictionary of int (neighbor indices) 1 if available 0 if already selected
    
    Returns
    -------
    update_nn: dicitonary of list with all the nodes 0 removed
    """
    updated_nn = dict()
    for k,x in nn.items():
        updated_x = [i for i in x if all_nodes.get(i) == 1]
        updated_nn[k] = updated_x
    return updated_nn

def clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1):
    """
    Clumping algorithm:
    1: Rank nodes by degree.
    2: For the node with highest degree, remove all 1st degree neighbors
    3: For the next highest ranking node take all remaining neighbors
    4: Expensively recompute the nn dictionary removing already used nodes
    selected nieghbors, and recompute nod rankings by remaining degrees 
    """

    # initialization before recursion
    if clumps is None:
        clumps = dict()
    if available_nodes  is None:
        available_nodes  = {x:1 for x in nn.keys()}
    #print(clumps)
    
    # Always re-sort to find highest degree node.
    # knn is dictionary of node:degree    
    knn = {k:len(v) for k,v in nn.items() if len(v) > min_degree}
    knn = dict(sorted(knn.items(), key=lambda item: item[1],reverse = True))
    #print(knn.items())
    # The first node is the largest
    if len(knn.items()) > 0:    
        node = next(iter(knn))
       
        # check that top node is still available
        if available_nodes.get(node) == 1:
            # xs are all its 1st degree neighbors
            xs = nn[node]
            xs = [x for x in xs if available_nodes .get(x) == 1] + [node]
            if len(xs) > min_degree:
                clumps[node] = xs
                for x in xs:
                    available_nodes[x] = 0
            # now remove all used nodes
            del nn[node]
            nn = recompute_nn(nn, available_nodes)
            # recall again using udpated nn 
            return clump_graph_expensive(nn=nn, available_nodes  = available_nodes , clumps=clumps, min_degree =min_degree)
        else: 
            del nn[node]
            nn = recompute_nn(nn, available_nodes)
            return clump_graph_expensive(nn=nn, available_nodes  =available_nodes , clumps=clumps, min_degree =min_degree)
    else:
        return clumps


def clump_graph_expensive_by_component(G):

    """
    Avoid expensive resorts by splitting by component
    """
    import networkx as nx
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    cg_all = list()
    for g in S:
        nn = dict()
        for i,j in g.edges:
            if i!=j:
                nn.setdefault(i,[]).append(j)
                nn.setdefault(j,[]).append(i)
        cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
        cg_all.append(cg_exp)
    cg_exp = dict()
    for d in cg_all:
        cg_exp.update(d)
    return cg_exp


def clump_component_expensive(g):
    nn = dict()
    for i,j in g.edges:
        if i!=j:
            nn.setdefault(i,[]).append(j)
            nn.setdefault(j,[]).append(i)
    sub_clumping = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
    return sub_clumping


def clump_graph_expensive_by_component_parmap(G, cpus = 2):
    import parmap
    import networkx as nx
    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    cg_all = parmap.map(clump_component_expensive, S, pm_processes = cpus, pm_pbar = True)
    cg_exp = dict()
    for d in cg_all:
        cg_exp.update(d)
    return cg_exp


# def clump_components_with_networkx_parmap(G, cpus = 2):
#     import networkx as nx
#     import parmap
#     S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
#     cg_all = parmap.map(clump_with_networkx,S,pm_processes = cpus, pm_pbar = True)
#     cg_exp = dict()
#     for d in cg_all:
#         cg_exp.update(d)
#     return cg_exp

# def clump_with_networkx(g, clumps = None):
#     import networkx as nx
#     if clumps is None:
#         clumps = dict()
#     if len(g.nodes) > 1:
#         degrees = list(g.degree())
#         degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
#         node_x = degrees[0][0]
#         if degrees[0][1] > 1:
#             neighbors_of_x = list(g.neighbors(node_x))
#             clumps[node_x] = neighbors_of_x + [node_x]
#             print(clumps)
#             for n in neighbors_of_x + [node_x]:
#                 g.remove_node(n)
#             return clump_with_networkx(g=g, clumps = clumps)
#         else:
#             return clumps
#     else:
#         return clumps

def viz(cg, G, num = 1, figname = None):
    """
    from clumpty.clump import clump_graph, clump_graph_expensive
    cg_basic = clump_graph(nn, min_degree = 1)
    cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
    viz(cg_exp, num = 2)
    viz(cg_basic, num = 1)
    """
    import networkx as nx
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
        nx.draw(g, pos, node_size=5, node_color=c, vmin=0.0, vmax=1.0, with_labels=False)
    
    if figname is None:
        figname = f'test_clumping_{num}.pdf'

    print(figname)
    plt.savefig(figname)
