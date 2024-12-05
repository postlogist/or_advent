param num_customers;
param num_warehouses;

set CUSTOMERS := 1..num_customers;
set WAREHOUSES := 1..num_warehouses;

param fixed_cost{WAREHOUSES};
param capacity {WAREHOUSES};
param demand {CUSTOMERS};

param allocation_cost{CUSTOMERS, WAREHOUSES};

var open {WAREHOUSES} binary;
var allocate {CUSTOMERS, WAREHOUSES} binary;
var source {CUSTOMERS, WAREHOUSES} >=0;


# A hack to prevent infeasible allocation of customers with large demand
param max_capacity := max {w in WAREHOUSES} capacity[w];

subject to AllocateToSource {c in CUSTOMERS, w in WAREHOUSES}:
    source[c, w] <= allocate[c, w] * demand[c];

subject to AllocateToOpen {w in WAREHOUSES, c in CUSTOMERS}:
    allocate[c, w] <= open[w];

subject to Demand {c in CUSTOMERS}: # all demand must be satisfied
    sum {w in WAREHOUSES} source[c, w] = demand[c]; 


/*
subject to AllocateSmall {c in CUSTOMERS : demand[c] <= max_capacity}: # otherwise allocation of customers 11 and 34 is infeasible
    sum {w in WAREHOUSES} allocate[c, w] = 1; 

subject to AllocateBig {c in CUSTOMERS : demand[c] > max_capacity}: # otherwise allocation of customers 11 and 34 is infeasible
    sum {w in WAREHOUSES} allocate[c, w] >= 1; 
*/


subject to Capacity {w in WAREHOUSES}:
    sum {c in CUSTOMERS} source[c, w] <= capacity[w];


minimize TotalCost:
    sum {w in WAREHOUSES} (fixed_cost[w] * open[w] + sum{c in CUSTOMERS} allocate[c, w] * allocation_cost[c, w]);


