#param num_items;

set BINS := 1..num_items;
set ITEMS := 1..num_items;

param bin_size;

param item_size{ITEMS}; 


var use{BINS} binary;
var put{i in ITEMS, b in BINS : i <= b} binary;
#var put{i in ITEMS, b in BINS} binary;

subject to BinCapacity {b in BINS}:
    sum {i in ITEMS: i <= b} put[i, b] * item_size[i] <= bin_size * use[b];
#    sum {i in ITEMS} put[i, b] * item_size[i] <= bin_size * use[b];

subject to PutAll {i in ITEMS}:
    sum {b in BINS: i <= b} put[i, b] = 1;
    #sum {b in BINS} put[i, b] = 1;

minimize NumBins:
    sum {b in BINS} use[b];

