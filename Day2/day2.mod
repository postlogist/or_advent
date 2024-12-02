param N;
param first;
param last;

set CITIES := 1..N;
set LINKS within {CITIES, CITIES};
param fuel_budget; # max fuel cost

param distance{LINKS};
param fuel_cost{LINKS};


var z {o in CITIES, d in CITIES : (o, d) in LINKS} binary; # flow from o to d



minimize TotalDistance:
    sum {o in CITIES, d in CITIES : (o, d) in LINKS} z[o, d] * distance[o, d];


subject to MaxFuel:
    sum {o in CITIES, d in CITIES : (o, d) in LINKS} z[o, d] * fuel_cost[o, d] <= fuel_budget;

subject to FlowConservation {c in CITIES : c != first and c != last}:
    sum {o in CITIES : (o, c) in LINKS } z[o, c] = sum {d in CITIES : (c, d) in LINKS} z[c, d];

subject to Depart:
    sum {d in CITIES: (first, d) in LINKS} z[first, d]= 1;

subject to Arrive:
    sum {o in CITIES: (o, last) in LINKS} z[o, last] = 1;

