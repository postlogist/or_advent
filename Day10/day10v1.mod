param num_components;
param num_links;

set COMPONENTS := 1..num_components;  
set LINKS within {COMPONENTS, COMPONENTS};  

var x {COMPONENTS} integer >= 1, <= card(COMPONENTS);  # Component's position on the line
var c {1..card(COMPONENTS)} >= 0, <= card(COMPONENTS);  # Number of crossings

# Unique positions
subject to Unique_Positions {i in COMPONENTS, j in COMPONENTS: i < j}:
    x[i] != x[j];

# Number of crossings
subject to Count_Crossings {k in 1..card(COMPONENTS), (i, j) in LINKS}:
    c[k] >= (x[i] - k) * (k - x[j]);  # Condition for crossing a line through k

# Objective
minimize Max_Crossings:
    max {k in 1..card(COMPONENTS)} c[k];

# Objective
minimize Sum_Crossings:
    sum {k in 1..card(COMPONENTS)} c[k];
