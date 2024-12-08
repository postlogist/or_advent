set ALL_ITEMS := 1..num_items;
param packed{ALL_ITEMS} default 0;
param item_size{ALL_ITEMS};
param bin_size;

#set ITEMS := setof {i in ALL_ITEMS: packed[i] < 0.5} i;
set ITEMS;

var put{i in ITEMS} binary;

subject to BinCapacity:
    sum {i in ITEMS} put[i] * item_size[i] <= bin_size;

maximize UsedSpace:
    sum {i in ITEMS} put[i] * item_size[i];



