# AMPL Model for Minimum Cost Subgraph Connecting Hubs (MTZ Approach)
param N;
# Sets and Parameters
set NODES := 1..N;                      # Set of nodes
set EDGES within {NODES, NODES};# Set of possible edges
param cost {EDGES};             # Cost of connecting nodes
set HUBS within NODES;          # Nodes (hubs) that must be connected

# Variables
var x {EDGES} binary;           # 1 if the edge is included in the solution; 0 otherwise
var y {NODES} binary;           # 1 if the node is used; 0 otherwise
var u {NODES} >= 0, <= card(NODES); # Order number of the node in the spanning tree

# Objective
minimize TotalCost:
    sum { (i, j) in EDGES } cost[i, j] * x[i, j];

# Constraints

# 1. All hubs must be connected
s.t. ConnectHubs {h in HUBS}:
    y[h] = 1;

# 2. A node is considered connected if at least one edge is incident to it
s.t. NodeUsage {i in NODES}:
    sum { (i, j) in EDGES } x[i, j] + sum { (j, i) in EDGES } x[j, i] >= y[i];

# 3. Tree constraint: the edges must connect nodes without forming cycles
s.t. TreeConstraint:
    sum { (i, j) in EDGES } x[i, j] = sum {i in NODES} y[i] - 1;


# 5. Order numbers of nodes to ensure connectivity (MTZ)
s.t. MTZ_Constraint {i in NODES, j in NODES: (i, j) in EDGES and i != j}:
    u[i] - u[j] + card(NODES) * x[i, j] <= card(NODES) - 1;

# 6. Order numbers for hub nodes
s.t. HubOrderConstraint {h in HUBS}:
    u[h] >= 1;

# 7. Connectivity of all hubs into a single component
# Ensure all hubs are connected via intermediate nodes if necessary
s.t. HubConnectivityFlow {h1 in HUBS, h2 in HUBS: h1 != h2}:
    u[h1] - u[h2] + card(HUBS) * (1 - sum { (i, j) in EDGES: i == h1 || j == h1 || i == h2 || j == h2 } x[i, j]) <= card(HUBS) - 1;

