
# clumptydumpty

## Usage

```python 
import pandas as pd
df = pd.read_csv("clumpty/tests/nn.csv")
edges = df.to_dict('split')['data']
nn = dict()
for i,j in edges:
    nn.setdefault(i,[]).append(j)
    nn.setdefault(j,[]).append(i)

from clumpty.clump import clump_graph, clump_graph_expensive
cg_basic = clump_graph(nn, min_degree = 1)
cg_exp = clump_graph_expensive(nn, available_nodes = None, clumps = None, min_degree = 1)
```
## Functions

### clump_graph

This function implements a clumping algorithm with optional enforcement of a minimum degree threshold. 

The steps are as follows:

1. It ranks nodes by their degree (number of connections).
Starting with the highest degree node, it removes all first degree neighbors (nodes directly connected to it).
2. It then proceeds to the next highest degree node, taking into account the remaining neighbors.
If the min_degree parameter is specified and greater than 1, it filters nodes based on this threshold.
3. The output is a dictionary clumps where each key is a node (used as a "clump" representative) and its value is a list of the nodes in the clump (including itselt).

### clump_graph_expensive

This function is a more computationally intensive version of the clump_graph function. 

It performs a similar process but includes a mechanism to dynamically update the neighbor dictionary (nn) as nodes are selected and become unavailable. This update is done using the recompute_nn helper function to ensure that the graph reflects the current availability of nodes. The function is recursive, meaning it calls itself with the updated graph data until no more clumps can be formed (i.e., when no nodes meet the degree threshold).

Key Mechanisms:

* Initialization: It checks if the clumps and available_nodes dictionaries are None (i.e., not yet created) and initializes them if necessary.
* Node Selection and Clump Formation: It identifies the highest degree node still marked as available, forms a clump including this node and its available neighbors, and then updates their availability.
* Recursion: After updating the neighbor data and the availability status of nodes, it calls itself with the updated parameters to continue the clumping process until no nodes are left to process.

These functions together create a utility for grouping nodes in a graph based on their connectivity, potentially suitable for tasks like community detection, clustering, or simplifying graph topology for further analysis.


