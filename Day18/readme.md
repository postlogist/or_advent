# P18: call me!

## 🧠 The problem

Hey, MORgan here, a network design consultant for 🌐 VerizOR.

My job is to ensure that we connect 📡 specific key locations (like cities, servers, or data centers) in the most cost-effective way possible.

However, we need to ensure that our connections form a network 🔗, and we want to minimize the total cost of laying cables 🛠️💵.

📋 Here’s what we know:

We have a bunch of nodes interconnected 🖧, and each connection has an associated cost (the expense of laying a cable between two nodes).
Some of the nodes are terminals 🔑, which must be connected together.
We can use other non-terminal vertices as intermediate connection points if necessary.
The goal is to find the minimum-cost subgraph that connects all terminal vertices directly or indirectly while satisfying the network constraint.

Can you help me solve this problem? 🧩

Let’s connect efficiently! 🌟

Here you can find an instance of this problem.

PS: if costs are close, how will you decide between multiple solutions?

# Analysis

This model implements a flow-based connectivity approach for solving the Minimum Cost Steiner Tree Problem. The goal is to find a minimum-cost subgraph that connects a subset of hub nodes, while ensuring connectivity, adhering to tree properties, and satisfying various constraints.

Problem Overview
The Steiner Tree Problem involves:

Connecting a given set of hub nodes (HUBS) in a graph.
Ensuring that the resulting subgraph is connected and forms a tree (acyclic).
Minimizing the total cost of the edges included in the solution.

Decision Variables
x[(i, j)]: Binary variable indicating whether edge (i, j) is included in the solution (1 if included, 0 otherwise).
y[i]: Binary variable indicating whether node i is used in the solution (1 if used, 0 otherwise).
flow[(i, j)]: Continuous variable representing the flow through edge (i, j) to ensure connectivity between hub nodes (bounded between 0 and the number of hubs minus one).

Input Parameters
N: Total number of nodes.
NODES: Set of nodes in the graph.
EDGES: Set of possible edges between nodes.
cost[(i, j)]: The cost of using edge (i, j).
HUBS: Subset of nodes that must be connected (key nodes in the Steiner Tree problem).
source_hub: A designated starting point among the hub nodes for flow-based connectivity.
card(HUBS): Number of hub nodes.

Objective
Minimize Total Cost
The objective function minimizes the total cost of the edges included in the solution:

$$ \text{minimize} \; \text{TotalCost} = \sum\_{(i, j) \in \text{EDGES}} \text{cost}[i, j] \cdot x[i, j] $$

Constraints

1. Hub Connectivity
   ConnectHubs: Ensures that all nodes in the hub set are included in the solution:

$$ y[h] = 1 \quad \forall h \in \text{HUBS} $$

2. Node-Edge Relationship
   NodeUsage: Ensures that if a node is used (y[i] = 1), then at least one edge incident to it must be included:

$$ \sum*{(i, j) \in \text{EDGES}} x[i, j] + \sum*{(j, i) \in \text{EDGES}} x[j, i] \geq y[i] \quad \forall i \in \text{NODES} $$

3. Tree Structure
   TreeConstraint: Ensures the tree property by ensuring the total number of included edges equals the number of used nodes minus one:
   $$ \sum*{(i, j) \in \text{EDGES}} x[i, j] = \sum*{i \in \text{NODES}} y[i] - 1$$

4. Flow-Based Connectivity
   FlowConservationSource: Ensures that the flow originating from the source hub equals the total number of hubs minus one:

$$\sum_{(source\_hub, j) \in \text{EDGES}} \text{flow}[source\_hub, j] - \sum_{(j, source\_hub) \in \text{EDGES}} \text{flow}[j, source\_hub] = \text{card}(\text{HUBS}) - 1$$

FlowConservationOthers: Enforces flow conservation for non-hub nodes (flow into a node equals flow out of it):
$$ \sum*{(j, i) \in \text{EDGES}} \text{flow}[j, i] = \sum*{(i, j) \in \text{EDGES}} \text{flow}[i, j] \quad \forall i \in \text{NODES} \setminus \text{HUBS} $$

FlowToHubs: Ensures each hub (except the source*hub) has a net inflow of exactly one unit of flow:
$$ \sum*{(j, h) \in \text{EDGES}} \text{flow}[j, h] - \sum\_{(h, j) \in \text{EDGES}} \text{flow}[h, j] = 1 \quad \forall h \in \text{HUBS} \setminus \{ \text{source_hub} \} $$

FlowCapacity: Restricts flow on an edge to exist only if the edge is included in the solution:
$$ \text{flow}[i, j] \leq (\text{card}(\text{HUBS}) - 1) \cdot x[i, j] \quad \forall (i, j) \in \text{EDGES} $$

5. Edge-Node Relationship
   IncludeEdge1: If an edge (i, j) is included, node j must be used:

$$x[i, j] \leq y[j]$$

IncludeEdge2: If an edge (i, j) is included, node i must be used:
$$x[j, i] \leq y[i]$$

6. Unidirectional Edges
   OneDirection: Ensures edges are considered only in one direction:

$$x[i, j] + x[j, i] \leq 1 \quad \forall (i, j) \in \text{EDGES}$$

Overall Logic
The model constructs a cost-optimal tree subgraph that connects all specified hub nodes (HUBS) while ensuring:

Connectivity: Flow-based constraints ensure all hubs are part of a single connected component with correct routing.
Tree Structure: The tree constraint and flow-based structure prevent cycles and minimize the number of edges used.
Edge-Node Relationship: Constraints ensure consistency between edge inclusion and node activation.
Cost Minimization: The objective function minimizes the total edge connection costs over the solution.
By combining flow-based connectivity with tree property enforcement, this formulation guarantees a minimum-cost, acyclic graph that connects all HUBS.
