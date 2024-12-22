# P21: for the environment

## 🧠 The problem

Today I'm the 🌱 Environmental Risk Management Officer at EnergyOR, a power plant company.

📈 The challenge:

Our company is expanding its operations, and we need to determine the best locations for 25 facilities (e.g., power plants or waste treatment centers).

However, these facilities emit noise 🔊, heat 🌡️, or pollutants 🌫️, so their placement requires careful planning.

🚧 Key considerations:

We must strategically locate these facilities as far as possible from:

🏫 Schools
🏡 Residential areas
🌳 Other sensitive zones
⚠️ The risks of poor facility placement:

Community Resistance: Complaints, protests, and legal actions ⚖️
Environmental Impact: Health risks and reduced quality of life 🌍
Operational Challenges: Costly retrofits or relocations due to public outcry 💸
🗺️ What we know:

A list of sensitive entities affected by power plant placement 🏠🏫
A list of potential facility locations 📍
A distance matrix 📏 among these points
🎯 Our goal is to maximize the sum of the minimum distances between that set of 25 facilities and the entities.

Can you help me solve this problem? 🧩

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7276591834271739905-WX9N)

## Analysis

This looks like a p-median problem with a twist

Variables:

- xij - assignment of a sensitive entity j to a facility i
- yi - auxiliary to count used facilities
- min_distance[i] - minimum distance for each facility

parameters:
dij - distance from the facility i to the entity j
min_distance[i] - minimum distance for the facility i
p - the number of facilities to be placed

Constraints:

- Linking x and y: yi <= sum xij
- The number of facilities: sum y[i] = p
- All entities are assigned to a facility ?

Objective:
to maximize the sum of minimum distances for each facility

There's no difference in the entity assignments in the current formulation. The objective considers only the minimum distances.
That makes sense baecause when we place a waste incinerator, it affetcs everyone nearby, not only those who are serviced by the facility.

Perhaps we can add some capacity constraint to the facility. For example, each facility can't handle more than |entities|/p entities.
