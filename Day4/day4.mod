param n_rooms;
param n_classes;
param n_teachers;
param n_periods;

set CLASSES := 1..n_classes;
set ROOMS := 1..n_rooms;
set TEACHERS := 1..n_teachers;
set PERIODS := 1..n_periods;

param requirement{ROOMS, CLASSES, TEACHERS}; # the number of required meetings for class and teacher in each room


var assign {ROOMS, CLASSES, TEACHERS, PERIODS} binary;

var teacher_clashes {j in TEACHERS, t in PERIODS} >=0;
var class_clashes {i in CLASSES, t in PERIODS} >=0;
var room_clashes {r in ROOMS, t in PERIODS} >=0;
var missed_requirements {r in ROOMS, i in CLASSES, j in TEACHERS} >=0;



subject to OneTeacher {j in TEACHERS, t in PERIODS}:
    sum {r in ROOMS, i in CLASSES} assign[r, i, j, t] <= 1 + teacher_clashes[j, t];

subject to OneClass {i in CLASSES, t in PERIODS}:
    sum {r in ROOMS, j in TEACHERS} assign[r, i, j, t] <= 1 + class_clashes[i, t];

subject to OneRoom {r in ROOMS, t in PERIODS}:
    sum {i in CLASSES, j in TEACHERS} assign[r, i, j, t] <= 1 + room_clashes[r, t];

subject to Meetings {r in ROOMS, i in CLASSES, j in TEACHERS}:
    sum {t in PERIODS} assign[r, i, j, t] = requirement[r, i, j] - missed_requirements[r, i, j];



minimize TotalClashes:
    sum {j in TEACHERS, t in PERIODS} teacher_clashes[j, t] +
    sum {i in CLASSES, t in PERIODS} class_clashes[i, t] +
    sum {r in ROOMS, t in PERIODS} room_clashes[r, t] +
    sum {r in ROOMS, i in CLASSES, j in TEACHERS} missed_requirements[r, i, j];
