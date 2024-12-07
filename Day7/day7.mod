param num_products; # number of products to ship
param num_subsets; # number of product subsets


set SUBSETS := 1 .. num_subsets; 
set PRODUCTS := 1 .. num_products;

set INCLUDED {SUBSETS} within PRODUCTS; # set of included products for each subset in


var pick{SUBSETS} binary;
param cost {SUBSETS};


minimize TotalCost:
    sum {s in SUBSETS} pick[s] * cost[s];


subject to Cover {p in PRODUCTS} :
    sum {s in SUBSETS : p in INCLUDED[s]} pick[s] = 1;

 

