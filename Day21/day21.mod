set FACILITIES; # Potential facility locations
set ENTITIES; # sensitive entities

param p; # The number of facilities placed

param capacity{FACILITIES} := ceil(card(ENTITIES) / p); # max. number of entities allocated to a facility

param distance{FACILITIES, ENTITIES};

param min_distance {i in FACILITIES} := min {j in ENTITIES} distance[i, j];

var y{FACILITIES} binary; # Facility placed at a location

var x{FACILITIES, ENTITIES} binary; # Entity is allocated to a facility


s.t. PlaceThenAllocate { i in FACILITIES} :
    y[i] <= sum {j in ENTITIES} x[i, j];

s.t. Capacity { i in FACILITIES} :
    sum {j in ENTITIES} x[i, j] <= y[i] * capacity[i];


s.t. AllocateAll {j in ENTITIES} :
    sum {i in FACILITIES} x[i, j] = 1;

s.t. NumberOfFacilities:
    sum {i in FACILITIES} y[i] = p;

maximize SumMinDistances:
    sum {i in FACILITIES} min_distance[i] * y[i];
