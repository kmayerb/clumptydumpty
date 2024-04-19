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

def clump_graph(nn, min_degree = 1):
    """
    Clumping algorithm:
    1: Rank nodes by degree.
    2: For the node with highest degree, remove all 1st degree neighbors
    3: For the next highest ranking node take all remaining neighbors
    4: Optionally if expensive is True, recompute the nn dictionary removing already
    selected nieghbors, and recompute nod rankings by remaining degrees 
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
    # The first node is the largest
    if len(knn.items()) > 0:    
        node = next(iter(knn))
       
        # check that top node is still available
        if available_nodes .get(node) == 1:
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
