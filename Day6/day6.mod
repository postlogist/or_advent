param num_segments; # number of rail segments to cover
param num_contracts; # number of contracts


set CONTRACTS := 1 .. num_contracts; 
set SEGMENTS := 1 .. num_segments;

set INCLUDED {CONTRACTS} within SEGMENTS; # set of included segments for each contract

#param num_included {CONTRACTS};


var pick{CONTRACTS} binary;
param cost {CONTRACTS};


minimize TotalCost:
    sum {c in CONTRACTS} pick[c] * cost[c];


subject to Cover {s in SEGMENTS} :
    sum {c in CONTRACTS : s in INCLUDED[c]} pick[c] >= 1;

 

