# P4: Optimal timetables

## 🧠 The problem

Hi, I'm SalvadOR, responsible for creating a school timetable to organize classes, teachers, and rooms for an upcoming semester.

We have some strict requirements to meet. This is a very hard problem we face every year, and I need your help to design an optimal timetable.

Here's the situation:

There are 4 classes, each requiring specific teaching sessions.
There are 4 teachers, and each teacher has assigned subjects to teach.
There are 4 rooms, and only one class can occupy a room during any given period.
The timetable spans 30 periods, and we must ensure that all requirements are met without any conflicts or overlaps.
I desperately need a timetable that satisfies all requirements (each class meets with the right teacher in the right room the required number of times), avoiding any type of clashes such as double-booking a teacher, room, or class during the same period.

We say a timetable is optimized when it minimizes idle periods and maximizes resource utilization (teachers and rooms).

Can you help me solve this problem?

Here you can find an instance of this problem.

## Analysis

The decision is an assignment of a specific teacher to a specific class in a specific room in a specific period.

So it has to have 4 indices:

$$ x_ijkt $$

Constraints:

- A teacher can be assigned to one class-room combination in each period.

- A class can be taught by just one teacher in one room in each period.

- A room can be assigned to only one teacher and class in each period.

- The number of meetings for each class and teacher must be exactly as specified over the entire time span.

Objective:

It might be impossible to avoid all the conflicts, so we can assign a weight to each conflict type and minimize the weighted sum of the conflicts.

Importance of Classclashes is 1
Importance of Teacherclashes is 1
Importance of Roomclashes is 1
Importance of Blocks is 1
Importance of preference is 1
Importance of limits is 1
Importance of relations is 1
Importance of distribution is 0
