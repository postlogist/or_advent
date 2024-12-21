# P20: optimal hospital

## 🧠 The problem

Today I'm the Operations Manager at MayOR Clinic Hospital, the largest hospital considering its staff size 👩‍⚕️🩺.

We're in a rush to improve the layout of our facility. Patient transfers, staff movement, and medical equipment transport between departments are not optimized.

This inefficiency causes delays, increases workload on staff, and reduces the quality of patient care.

We're working on placing departments close to each other to minimize the cost of moving. For example:

Emergency Room must be close to the Radiology and Operating Rooms because of frequent patient transfers.
Pharmacy should be centrally located to minimize the time it takes for nurses to collect medications for patients.
ICU (Intensive Care Unit) and Laboratory need proximity to minimize delays in test results.
In a hospital, optimizing department layout can:

✨ Improve Patient Care: Minimize patient transfer times between critical departments (e.g., ER to OR).
⚡ Enhance Staff Efficiency: Reduce walking distances for nurses, doctors, and technicians.
💰 Save Costs: Lower the costs of equipment transport and streamline workflows.
So we started addressing this problem considering two factors:

The flow of movements between different departments
The distance we have between them
And with that information, we're building the travel costs.

Our goal is to minimize those costs 🏆.

Can you help me solve this problem? 🧩

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7275779510539632640-xWUR?utm_source=share&utm_medium=member_desktop)

Remember to...

Get the important things from the definition (objective function, constraints, decision variables)
Document your journey
Share your thoughs in my post for today (you'll recognize it easily)
Fill the form so I can give you the points for commenting to the post and other peers' ideas:

## Analysis

Parameters:

- distance between locations
- flow between facilities
- Variables:
- The assignment of facilities to locations (binaries) - a

Constraints:

- All facilities must be assigned
- At most one facility per locations

Objective:

- Minimize total travel distance: sum (all i1,j1, i2, j2) a[i1,j1] _ a[i2,j2] _ d[j1,j2] \* f[i1,i2];
