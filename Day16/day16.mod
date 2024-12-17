# Sets
set TASKS := 1..num_tasks;                  # Set of tasks
set STEPS := 1..num_tasks;                  # Number of steps in a sequence of tasks
set LINKS within {TASKS, TASKS};            # Valid links (i, j) between tasks

# Parameters
param start_time {TASKS};                   # Start time of each task
param end_time {TASKS};                     # End time of each task
param transition_time {TASKS, TASKS} default 9999; # Transition time between tasks
param fixed_cost {TASKS}; # not used

# Derived Set
set CREWS := 1..num_crews;

# Variables
var x {TASKS, CREWS, STEPS} binary;         # Task i is assigned to crew c at step s
var use_crew {CREWS} binary;                # Whether crew c is used

# Objective: Minimize the total number of crews used
minimize TotalCrews:
    sum {c in CREWS} use_crew[c];

# Constraints

# 1. Each task must be assigned exactly once
s.t. AssignEachTask {i in TASKS}:
    sum {c in CREWS, s in STEPS} x[i, c, s] = 1;

# 2. A crew must be marked as used if it has at least one task
s.t. CrewUsage {c in CREWS}:
    sum {i in TASKS, s in STEPS} x[i, c, s] <= card(TASKS) * use_crew[c];

# 3. Each step can have at most one task per crew
s.t. StepLimit {c in CREWS, s in STEPS}:
    sum {i in TASKS} x[i, c, s] <= 1;

# 4. Sequence Feasibility: Tasks must follow valid transitions in LINKS
s.t. SequenceFeasibility {c in CREWS, s in 2..num_tasks, j in TASKS}:
    x[j, c, s] <= sum {(i, j) in LINKS} x[i, c, s-1];    
    

# 5. Transition Times: Ensure no overlap and sufficient transition time between tasks
s.t. TransitionTime {c in CREWS, s in 2..num_tasks, (i, j) in LINKS }: #i in TASKS, j in TASKS: i != j
    (x[i, c, s-1] == 1 and start_time[j] >= end_time[i] + transition_time[i, j]) ==>
        (x[j, c, s] <= 1) else x[j, c, s] <= 0;
    #start_time[j] * x[j, c, s] >= (end_time[i] + transition_time[i, j]) * x[i, c, s-1];

# 6. Symmetry Breaking: Enforce ordering of crew usage to reduce symmetry
s.t. SymmetryBreaking {c in CREWS: c < num_crews}:
    use_crew[c] >= use_crew[c+1];

# Next step is used only when the previous step was used
s.t. SequentialSteps {c in CREWS, s in 2..num_tasks}:
    sum {i in TASKS} x[i, c, s]  <= sum {i in TASKS} x[i, c, s-1];