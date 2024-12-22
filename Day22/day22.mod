# Job scheduling problem
param n_jobs; # Number of jobs (cars)

param n_stages; # Number of processing stages

set JOBS := 0..n_jobs-1; # Set of jobs

set STAGES := 0..n_stages-1; # Set of processing stages

param machine_required {JOBS, STAGES}; # machine for each step of a job

#set MACHINES := setof {j in JOBS, s in STAGES} m[j, s]; # set of machines

param p {JOBS, STAGES} >= 0; # Processing time of a job at a stage

# Upper bound of the time at each stage
param bigM := sum{j in JOBS, s in STAGES} p[j, s]; # bigM

#param H {s in STAGES} := sum{j in JOBS} p[j, s]; # This can be replaced with a more accurate estimate

# Variables
var start_time {j in JOBS, s in STAGES} >= 0, <= bigM; # Start time of a job at a stage

var end_time {j in JOBS, s in STAGES} >= 0, <= bigM; # End time of a job at a stage

#var makespan; # Total production time

# Binary variable for modeling job execution order
#var y {JOBS, JOBS, STAGES} binary;
#var y {JOBS, JOBS} binary;


# Constraints
# Sequence of tasks for a job
subject to sequence {j in JOBS, s in STAGES: s < n_stages-1}:
    start_time[j, s + 1] >= end_time[j, s];

# Processing time
subject to CompletionTime {j in JOBS, s in STAGES}:
    end_time[j, s] = start_time[j, s] + p[j, s];

/*
subject to no_overlap1 {(i,j) in JOBS cross JOBS, s in STAGES : i != j}:
    end_time[i, s] <= start_time[j, s] + bigM  * (1 - y[i, j, s]); #H[s]

subject to no_overlap2 {(i,j) in JOBS cross JOBS, s in STAGES: i != j}:    
    end_time[j, s] <= start_time[i, s] + bigM * y[i, j, s]; #H[s]
*/
/*
subject to no_overlap1 {(i,j) in JOBS cross JOBS, s in STAGES : i != j}:
    end_time[i, s] <= start_time[j, s] + bigM  * (1 - y[i, j]); #H[s]

subject to no_overlap2 {(i,j) in JOBS cross JOBS, s in STAGES: i != j}:    
    end_time[j, s] <= start_time[i, s] + bigM * y[i, j]; #H[s]
*/


subject to MachineDeconflict {s1 in STAGES, s2 in STAGES, (j1,j2) in JOBS cross JOBS: 
        j1 != j2 and machine_required[j1, s1] = machine_required[j2, s2] }:    
    (end_time[j1, s1] <= start_time[j2, s2] or end_time[j2, s2] <= start_time[j1, s1])
    and not
    (end_time[j1, s1] <= start_time[j2, s2] and end_time[j2, s2] <= start_time[j2, s1]);


/*
subject to finish_time {j in JOBS}:
    makespan >= end_time[j, n_stages-1];
*/


# Either i or j is the first job
/*
subject to Symmetry {(i,j) in JOBS cross JOBS, s in STAGES : i != j}:
    y[i, j, s] = 1 - y[j, i, s];
*/
/*
# Same sequence for all stages
subject to SameSequence {(i,j) in JOBS cross JOBS, s in STAGES : i != j}:
    y[i, j, s] = y[i, j, 0];

*/

/*
# Either i or j is the first job
subject to Symmetry {(i,j) in JOBS cross JOBS: i != j}:
    y[i, j] = 1 - y[j, i];
*/

# Objective function
#minimize Makespan: makespan;
minimize Makespan: max {j in JOBS} end_time[j, card(STAGES)-1];
