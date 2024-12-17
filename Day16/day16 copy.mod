set TASKS := 1 .. num_tasks;    # Set of tasks
set LINKS within {TASKS, TASKS};  # Set of possible links (i, j)
set CREWS := 1..num_crews;    # Set of crews

param start_time {TASKS};   # Start time of each task
param end_time {TASKS};     # End time of each task
param transition_time {LINKS}; # Transition time for each link (i, j)
param fixed_cost {TASKS}; # task fixed cost #not used

# Decision variables
var use_crew{CREWS} binary;
var x_first {TASKS, CREWS} binary; # First task assigned to the crew x_first[i, c] = 1 if crew c is assigned to task i as a first task
var x {TASKS, CREWS} binary;  # x[i, c] = 1 if crew c is assigned to task i
var y {LINKS, CREWS} binary;  # y[i, j, c] = 1 if crew c transitions from task i to task j

# Objective: Minimize the total number of crews used
minimize TotalCrews: sum {c in CREWS} use_crew[c];

# Constraints

# Crew use:
s.t. UseCrew {c in CREWS, i in TASKS} :
    x_first[i, c] + x[i, c] <= use_crew[c];

# Symmetry breaking:
s.t. Symmetry {c1 in CREWS, c2 in CREWS : c2 > c1}:
    use_crew[c2] <= use_crew[c1];

# Each task must be assigned to exactly one crew
s.t. AssignOneCrew {i in TASKS}:
    sum {c in CREWS} (x_first[i, c] + x[i, c]) = 1;

# Only one first task is assigned:
s.t. FirstOne{c in CREWS}:
    sum {i in TASKS} x_first[i, c] <= 1;


# Can't assign transitions when the first task is not assigned
s.t. AssignTransitionFirst {c in CREWS, (i, j) in LINKS}:
    y[i, j, c] <= x_first[i, c];


# Can assign a transition to the team only if the origin of the transition is already assigned to the same team:
s.t. AssignTransition {c in CREWS, (i, j) in LINKS}:
    y[i, j, c] <= x[i, c] + x_first[i, c];


s.t. AssignDestination {c in CREWS, (i, j) in LINKS}:
    y[i, j, c] == x[j, c];

/*
# Can't assign task if there's no transition to it:
s.t. MustAssignTransition {c in CREWS, j in TASKS}:
    x[j, c] <= x_first[j, c] + sum {(i, j) in LINKS} y[i, j, c];

# Assign a destination task of the transition to the same team:
s.t. AssignDestination {c in CREWS, (i, j) in LINKS}:
    (y[i, j, c] == 1) ==> (x[j, c] == 1);
*/

# Can't assign a transition when there's not enough time to transition
s.t. EnoughTime {c in CREWS, (i, j) in LINKS}:
    #y[i, j, c] <= if (start_time[j] >= end_time[i] + transition_time[i, j]) then 1 else 0;
    (y[i, j, c] == 1) ==> start_time[j] >= end_time[i] + transition_time[i, j];

# No overlap between tasks assigned to the same crew
s.t. NoOverlap {c in CREWS, i in TASKS, j in TASKS: i != j}:
    ((x_first[i, c] + x[i, c]) == 1 and (x[j, c] + x_first[j, c]) == 1 /*and (i, j) not in LINKS*/) ==> 
        (start_time[j] >= end_time[i] /*or start_time[i] >= end_time[j]*/);
/*
# Ensure transitions match task assignments
s.t. MatchTransitions {i in TASKS, c in CREWS}:
    sum {j in TASKS: (i, j) in LINKS} y[i, j, c] 
    + sum {j in TASKS: (j, i) in LINKS} y[j, i, c] 
    <= 1;
*/