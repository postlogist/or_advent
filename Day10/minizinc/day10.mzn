include "globals.mzn";

% Number of components
int: N;
set of int: COMPONENTS = 1..N;

% Number of connections
int: C;
set of int: CONNECTIONS = 1..C;

% Connections
array[CONNECTIONS] of int: from;

array[CONNECTIONS] of int: to;

% Decision variables
array[COMPONENTS] of var COMPONENTS: position;
  
array[CONNECTIONS, CONNECTIONS] of var bool: crossings;
constraint alldifferent(position);

%% Crossings
constraint forall(c1, c2 in CONNECTIONS where c1 < c2)(
  let {
    var int: c1_v1 = position[from[c1]];
    var int: c1_v2 = position[to[c1]];
    var int: c2_v1 = position[from[c2]];
    var int: c2_v2 = position[to[c2]];
 
    var int: start1 = min([c1_v1, c1_v2]);
    var int: end1 = max([c1_v1, c1_v2]);
    var int: start2 = min([c2_v1, c2_v2]);
    var int: end2 = max([c2_v1, c2_v2]);
  } in
  
 
  ((start1 < start2 /\ start2 < end1 /\ end2 > end1)
  \/
  (start2 < start1 /\ start1 < end2 /\ end1 > end2)) = crossings[c1, c2]
 
);

% Symmetry breaking
constraint position[1] < position[N];

solve minimize sum(c1, c2 in CONNECTIONS where c1 < c2)(crossings[c1, c2]);

output ["number of crossings: \(_objective), layout: \(inverse(position))"];