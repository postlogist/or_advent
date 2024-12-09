include "globals.mzn";

% Input data
int: n;  % Number of items
int: bin_capacity;  % Capacity of each bin
array[1..n] of int: item_sizes;  % Sizes of the items

% Parameters specific to this instance
string: instance_id;  % Instance identifier
int: best_known_bins;  % Best known number of bins for this instance

% Variables
%int: max_bins = sum(item_sizes) div bin_capacity + 1;  % Upper bound on the number of bins
int: max_bins = n;  % Upper bound on the number of bins
array[1..n] of var 1..max_bins: bin_assignment;  % Bin assigned to each item
array[1..max_bins] of var 0..bin_capacity: bin_usage;  % Usage of each bin

% Constraints
% Ensure the capacity of each bin is not exceeded
constraint forall(b in 1..max_bins) (
  bin_usage[b] = sum([item_sizes[i] | i in 1..n where bin_assignment[i] == b])
);
constraint forall(b in 1..max_bins) (
  bin_usage[b] <= bin_capacity
);

% Minimize the number of bins used
var int: num_bins_used = max(bin_assignment);
solve minimize num_bins_used;

% Output
output [
  "Instance ID: ", show(instance_id), "\n",
  "Number of bins required: ", show(num_bins_used), "\n",
  "Smallest known number of bins: ", show(best_known_bins), "\n",
  "Item assignments: ", show(bin_assignment), "\n"
];
