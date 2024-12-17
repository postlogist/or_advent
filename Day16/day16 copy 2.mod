# Sets
set TASKS := 1..num_tasks;                             # Set of tasks
set LINKS within {TASKS, TASKS};       # Set of valid links (i, j) between tasks

# Parameters
param fixed_cost {TASKS};              # Fixed cost of each task, not used
param start_time {TASKS};              # Start time of each task
param end_time {TASKS};                # End time of each task
param transition_time {TASKS, TASKS} default 9999; # Transition time between tasks

# Derived Set
set CREWS := 1..num_crews;             # Index of crews

# Variables
var use_crew {CREWS} binary;                          # Whether a crew is used (binary)
var x {TASKS, CREWS} binary;                          # x[i, c] = 1 if task i is assigned to crew c
var y {LINKS, CREWS} binary;                          # y[i, j, c] = 1 if crew c transitions from task i to task j

# Objective: Minimize the total number of crews used
minimize TotalCrews: sum {c in CREWS} use_crew[c];

# Constraints

# 1. Each task must be assigned to exactly one crew
s.t. AssignOneCrew {i in TASKS}:
    sum {c in CREWS} x[i, c] = 1;

# 2. A crew must be marked as used if it has at least one task
s.t. CrewUsage {c in CREWS}:
    sum {i in TASKS} x[i, c] <= card(TASKS) * use_crew[c];

# 3. No overlap between tasks for the same crew
s.t. NoOverlap {c in CREWS, i in TASKS, j in TASKS: i != j}:
    x[i, c] + x[j, c] <= 1 
    or start_time[j] >= end_time[i] 
    or start_time[i] >= end_time[j];

# 4. If a transition link (i, j) is used, both tasks i and j must be assigned to the same crew
s.t. LinkConsistency1 {c in CREWS, (i, j) in LINKS}:
    y[i, j, c] <= x[i, c];
s.t. LinkConsistency2 {c in CREWS, (i, j) in LINKS}:    
    y[i, j, c] <= x[j, c];
s.t. LinkConsistency3 {c in CREWS, (i, j) in LINKS}:    
    y[i, j, c] >= x[i, c] + x[j, c] - 1;

# 5. Transition times must be respected when moving between tasks
s.t. TransitionTime {c in CREWS, (i, j) in LINKS}:
    y[i, j, c] * (start_time[j] - end_time[i]) >= transition_time[i, j];

# 6. Symmetry-breaking to improve solver performance
s.t. SymmetryBreaking {c1 in CREWS, c2 in CREWS: c2 > c1}:
    use_crew[c2] <= use_crew[c1];


# 7. Adjacent transitions
s.t. AdjacentTasks {i in TASKS, j in TASKS: i < j}:
    ()