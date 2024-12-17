param n;  # Number of planes

# Plane-specific parameters
param a{i in 1..n};  # Appearance time of plane i
param t{i in 1..n};  # Target landing time of plane i
param e{i in 1..n};  # Earliest landing time of plane i
param l{i in 1..n};  # Latest landing time of plane i
param c_early{i in 1..n};  # Cost per unit time for landing before target time
param c_late{i in 1..n};   # Cost per unit time for landing after target time

# Safety gap between planes
param g{i in 1..n, j in 1..n};  # Minimum safety gap if plane i lands before plane j

# Decision variables
var L{i in 1..n} >= e[i], <= l[i];  # Landing time of plane i
var y{i in 1..n, j in i+1..n} binary;  # Binary: 1 if plane i lands before plane j, 0 otherwise
var Ua{i in 1..n} >= 0;  # Time deviation from target landing time - above
var Ub{i in 1..n} >= 0;  # Time deviation from target landing time - below

# Objective: Minimize total penalty cost
minimize TotalPenalty: 
    sum {i in 1..n} (c_early[i] * Ub[i] + c_late[i] * Ua[i]);

# Constraints for time deviation
subject to DeviationAbove{i in 1..n}:
    Ua[i] >= L[i] - t[i];

subject to DeviationBelow{i in 1..n}:
    Ub[i] >= t[i] - L[i];

# Constraints

subject to SafetyGap{i in 1..n, j in i+1..n}: 
    L[j] >= L[i] + g[i, j] - (1 - y[i, j]) * (l[j] - e[i]);
    
subject to SafetyGapReverse{i in 1..n, j in i+1..n}:
    L[i] >= L[j] + g[j, i] - y[i, j] * (l[i] - e[j]);


/*# Enforce mutual exclusivity of landing order
subject to Exclusivity{i in 1..n, j in i+1..n}:
    y[i, j] + y[j, i] = 1;
*/
