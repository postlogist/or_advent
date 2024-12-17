# P17: landing safely

## 🧠 The problem

Hi, I'm SaqoOR, an Operations Manager at the busiest airport in the world: Dubai International Airport 🌍.

My primary goal is to ensure that all incoming aircraft land safely and efficiently, minimizing costs associated with delays or early arrivals ⏱️.

🚦 The complexity:

Managing the schedule of aircraft landings is challenging due to:

Safety separation times 🛑
Penalties for deviating from target landing times ⚠️
📋 The information we have...

For each plane:

An appearance time (when it enters the radar) 🕒
An earliest landing time (when it's technically possible to land) 🕘
A target landing time (the preferred time for optimal operations) ⏱️
A latest landing time (after which landing is completely infeasible) 🕛
💰 Costs, as landing earlier or later than the target time incurs penalties:

Cost per unit time before target time.
Cost per unit time after target time.
⏳ Separation times:

A minimum safety gap (in minutes) must be maintained between consecutive landings to ensure smooth operations and avoid collisions 🚨
These times depend on the pair of planes and their landing characteristics ✈️
🎯 The goal? Minimizing the total penalty costs 💵 while satisfying constraints ✅.

Can you help me solve this problem? 🧩

Let’s ensure safe skies and efficient operations at DXB! 🌟

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7274692349052542977-MqB8?utm_source=share&utm_medium=member_desktop)

# Analysis

Decision variables:
L, real - planned landing time for each plane
y[i,j], binary - order of landings, for safety gap constraint
Ua/Ub - auxiliary variables for deviations from the target landing time

Objective:
to minimize the sum of penalties for being late or early

Constraints:

- Ensure safety gap between planned landing times
- Bounds for L
