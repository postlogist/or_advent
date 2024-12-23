# Sets
param num_products;
set PRODUCTS := 0..num_products - 1;                     # Set of all candidate products (1..30)
set PAIRS = {i in PRODUCTS, j in PRODUCTS: i < j};  # All possible pairs

# Parameters
param distance{PAIRS};   # Distance matrix between products
param num_select;               # Number of products to select

param M := max{(i, j) in PAIRS} distance[i,j];

# Variables
var select{PRODUCTS} binary;         # 1 if product is selected, 0 otherwise
var min_dist;                        # Minimum distance between any selected pair

# Objective: Maximize the minimum distance between selected products
maximize max_min_dist: min_dist;

# Constraints
# Select exactly num_select products
subject to select_count:
    sum{i in PRODUCTS} select[i] = num_select;

# Min distance constraint
subject to min_distance_constraint{(i, j) in PAIRS}:
    min_dist <= distance[i,j]  + M * (2 - select[i] - select[j]);
#(select[i] == 1 and select[j] == 1) ==> 
#    (min_dist <= distance[i,j]); #didn't work
