param N; # the number of employees and tasks

set TASKS := 1..N;
set EMPLOYEES := 1..N;

param cost {TASKS, EMPLOYEES};

var assign {TASKS, EMPLOYEES} binary;
# var assign {TASKS, EMPLOYEES} >=0  <= 1; # works as well


minimize TotalCost:
    sum {e in EMPLOYEES, t in TASKS} assign[t, e] * cost[t, e];


subject to OneTaskOnly {e in EMPLOYEES}:
    sum {t in TASKS} assign[t, e] = 1;


subject to OneTaskOnly2 {t in TASKS} :
    sum {e in EMPLOYEES} assign[t, e] = 1;
