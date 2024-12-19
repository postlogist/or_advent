# AMPL Model for Minimum Cost Subgraph Connecting Hubs (Flow-Based Connectivity Approach)
param N; # number of nodes
# Sets and Parameters
set NODES := 1..N;                      # Set of nodes
set EDGES within {NODES, NODES};# Set of possible edges
param cost {EDGES};             # Cost of connecting nodes
set HUBS within NODES ordered;          # Nodes (hubs) that must be connected

# Variables
var x {EDGES} binary;           # 1 if the edge is included in the solution; 0 otherwise
var y {NODES} binary;           # 1 if the node is used; 0 otherwise
var flow {EDGES} >= 0 <= card(HUBS)-1;          # Flow between nodes to ensure connectivity

# Objective
minimize TotalCost:
    sum { (i, j) in EDGES } cost[i, j] * x[i, j];

# Constraints

# 1. All hubs must be connected
# Each hub must be used in the solution

s.t. ConnectHubs {h in HUBS}:
    y[h] = 1;

# 2. A node is considered connected if at least one edge is incident to it
# Ensure that if a node is used, it has at least one edge included in the solution
s.t. NodeUsage {i in NODES}:
    sum { (i, j) in EDGES } x[i, j] + sum { (j, i) in EDGES } x[j, i] >= y[i];

# 3. Tree constraint: the edges must connect nodes without forming cycles
# The total number of edges in the solution must equal the number of used nodes minus 1
s.t. TreeConstraint:
    sum { (i, j) in EDGES } x[i, j] = sum {i in NODES} y[i] - 1;


# 5. Flow conservation to ensure all hubs are connected
# Ensure that flow starts at one specific hub and flows to all other hubs
param source_hub := first(HUBS); # Choose one hub as the source of the flow
s.t. FlowConservationSource:
    sum { (source_hub, j) in EDGES } flow[source_hub, j] 
    - sum { (j, source_hub) in EDGES } flow[j, source_hub] = card(HUBS) - 1; # sum { (j, source_hub) in EDGES } flow[j, source_hub] - 

s.t. FlowConservationOthers {i in NODES diff HUBS}:
    sum { (j, i) in EDGES } flow[j, i] = sum { (i, j) in EDGES } flow[i, j]; #the flow must pass through to the hubs

# Ensure that each hub (except the source hub) has a net inflow of exactly 1 unit of flow
s.t. FlowToHubs {h in (HUBS diff {source_hub})}:
    sum { (j, h) in EDGES } flow[j, h] - sum { (h, j) in EDGES } flow[h, j] = 1;

# 6. Flow capacity constraint: flow can exist only if the edge is used
# Ensure that no flow can pass through an edge that is not included in the solution
s.t. FlowCapacity {(i, j) in EDGES}:
    flow[i, j] <= (card(HUBS) - 1) * x[i, j]; 

# 7. Tree connectivity constraint
# Ensure that the total flow equals the number of hubs minus 1 (required to connect all hubs)
/*s.t. TreeConnectivity:
    sum { (i, j) in EDGES } flow[i, j] = card(HUBS) - 1;*/

# Include edge => connect node
s.t. IncludeEdge1 {(i, j) in EDGES}:
    x[i, j] <= y[j];

s.t. IncludeEdge2 {(i, j) in EDGES}:
    x[j, i] <= y[i];

# Unidirectional edges
s.t. OneDirection {(i, j) in EDGES}:
    x[i, j] + x[j, i] <= 1;

