# P16: fly away

## 🧠 The problem

✈️ Today I'm a crew planner at QatOR Airways 🌍

I'm responsible for ensuring that all flights are adequately staffed 🧑‍✈️👩‍✈️ while minimizing costs.

🎯 My daily goal is to assign crew members to specific tasks while ensuring optimal resource utilization.

🚧 The complexity:

This is no easy task! Compliance with work-hour restrictions, rest requirements, and skill qualifications makes it challenging 😵‍💫.

(But let's skip those details for now! 😉)

📋 What I know:

The cost for operating a flight, along with its start and finish times 🕒
The cost for a crew going from one flight to another one 🚖
Since this is a daily task, I usually have a maximum of 8 minutes ⏱️ to complete it so I can send the crews to other members of my team.

Can you help me solve this problem? 🧩

Let’s optimize the crew schedules and keep the skies running smoothly! 🛫

Here you can find an instance of this problem.

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7274329961476358144-vyty?utm_source=share&utm_medium=member_desktop)

## Analysis

The decision variables are:

- assignments of the tasks to the teams
- assignments of the transitions to the teams
- auxiliary variables to count the number of teams used

The objective is to minimize the total number of teams used. Minimizing the total fixed cost associated with tasks is meaningless, since all the tasks must be assigned and the sum will always be the same. Such an objective would'n distinguish between the different task assignments.

The constraints:

- Each task must be assigned to a single team
- Auxiliary constraint linking task assignment and the use of teams
- Linking constraints for task assignments and transition assignments
- A team can be assigned a transition only when there's enough time between the end of the first task and the beginning of the next task
- For any two tasks assigned to a team there must be no overlap between them

## Results

Couldn't solve the original instance, it required 50 teams for 50 tasks.

Tested with some smaller instances, the solution seems to be adequate.
