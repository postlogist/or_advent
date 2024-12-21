param n; # number of facilities/locations

set FACILITIES := 1..n;
set LOCATIONS := 1..n;

var assign{FACILITIES, LOCATIONS} binary;
#var z{FACILITIES, FACILITIES, LOCATIONS, LOCATIONS} binary; #auxiliary variable for linearization

param distance{LOCATIONS, LOCATIONS};

param flow{FACILITIES, FACILITIES};



# Assign all facilities:
s.t. AssignAll {i in FACILITIES}:
    sum {j in LOCATIONS} assign[i, j] == 1;

# One facility per location
s.t. OnePerLocations {j in LOCATIONS}:
    sum{i in FACILITIES} assign[i, j] == 1;

/*
# link assign and z;
s.t. Link1 {i1 in FACILITIES, i2 in FACILITIES, j1 in LOCATIONS, j2 in LOCATIONS: i1 != i2 and j1 != j2}:
    z[i1, i2, j1, j2] <= assign[i1, j1];


s.t. Link2 {i1 in FACILITIES, i2 in FACILITIES, j1 in LOCATIONS, j2 in LOCATIONS: i1 != i2 and j1 != j2}:
    z[i1, i2, j1, j2] <= assign[i2, j2];

s.t. Link3 {i1 in FACILITIES, i2 in FACILITIES, j1 in LOCATIONS, j2 in LOCATIONS: i1 != i2 and j1 != j2}:
    z[i1, i2, j1, j2] >= assign[i1, j1] + assign[i2, j2] - 1;
*/

# Minimize total distance traveled:
minimize TotalDistance:
    sum {i1 in FACILITIES, i2 in FACILITIES, j1 in LOCATIONS, j2 in LOCATIONS: i1 != i2 and j1 != j2} 
        assign[i1, j1] * assign[i2, j2] * distance[j1, j2] * flow[i1, i2];
#        z[i1, i2, j1, j2] *  distance[j1, j2] * flow[i1, i2];

