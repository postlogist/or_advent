# Sets and Parameters
param num_products;
set PRODUCTS := 1..num_products;               # Set of products

param profit {PRODUCTS};    # Profit from promoting each product
param synergy {i in PRODUCTS, j in PRODUCTS: i < j}; # Synergy profit when two products are promoted
param cost {PRODUCTS};      # Promotion cost for each product
param budget;               # Total promotion budget

# Decision Variables
var promote {PRODUCTS} binary;  # 1 if product is promoted, 0 otherwise

# Objective Function
maximize TotalProfit:
    sum {i in PRODUCTS} profit[i] * promote[i] +
    sum {(i, j) in PRODUCTS cross PRODUCTS: i < j} synergy[i, j] * promote[i] * promote[j];

# Constraints
subject to BudgetConstraint:
    sum {i in PRODUCTS} cost[i] * promote[i] <= budget;

