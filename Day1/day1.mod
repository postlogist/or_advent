param N; # n events

set EVENTS := 1 .. N;
set ROOMS := 1 .. 16;

set CONFLICTS within {EVENTS, EVENTS};

var assign {e in EVENTS, r in ROOMS : e >= r} binary; # assign event e to room r. For symmetry breaking, assume that event number e can be assigned to room with number e or greater.
var use {r in ROOMS} binary;


subject to Use {e in EVENTS, r in ROOMS: e >= r}:
    assign[e, r] <= use[r];


subject to Conflict {r in ROOMS, (e1, e2) in CONFLICTS: e1 >= r and e2 >= r}:
    assign[e1, r] + assign[e2, r] <= 1;


subject to Assign {e in EVENTS}:
    sum {r in ROOMS : e >= r} assign[e, r] = 1;

minimize NumberOfRooms:
    sum {r in ROOMS} use[r];



