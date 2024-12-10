param num_components;
param num_links;

set COMPONENTS := 1..num_components;  
set LINKS within {COMPONENTS, COMPONENTS};  

# Variables
var x {COMPONENTS} integer >= 1, <= card(COMPONENTS);  # Component's position on the line
var c {1..card(COMPONENTS)} >= 0, <= card(COMPONENTS);  # Number of crossings
var b {1..card(COMPONENTS), (i, j) in LINKS} binary;    # Binary variable for crossings

# Unique positions
subject to Unique_Positions {i in COMPONENTS, j in COMPONENTS: i < j}:
    x[i] != x[j];

/* didn't work

# Try to improve the LB
subject to SumOfPositions:
    sum {k in 1..num_components} x[k] == (num_components * (num_components + 1) / 2);  # the sum of the positions should be always the sum of series of 1..num_components
*/

# Logical conditions for crossings
subject to Crossing_Condition1 {k in 1..card(COMPONENTS), (i, j) in LINKS}:
    ((x[i] < k and x[j] > k) 
    or
    (x[j] < k and x[i] > k)) ==> b[k, i, j] == 1;


# Count crossings
subject to Count_Crossings {k in 1..card(COMPONENTS)}:
    c[k] = sum {(i, j) in LINKS} b[k, i, j];

# Objective
minimize Max_Crossings:
    max {k in 1..card(COMPONENTS)} c[k];

# Objective
minimize Sum_Crossings:
    sum {k in 1..card(COMPONENTS)} c[k];
