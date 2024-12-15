# P13: send it cheap!

## 🧠 The problem

Today I'm a logistic planner at SC NetwORks 🚚.

We're facing a tough challenge distributing goods from a central warehouse to multiple customer locations.

Our goal?

🔑 Minimize the total cost of shipping goods while satisfying all customer demands.

But here’s the twist: the cost of transporting goods across routes is cheaper per unit as the total amount increases 📉. This showcases economies of scale 💡.

The information we usually manage:

🧾 The number of customers to serve and their demand.
🚦 A matrix of potential routes for shipping goods.
🧮 A cost function.
The cost function is like this:

f(x*ij) = -a_ij * x*ij^2 + b_ij * x_ij + c_ij

Here’s what each part means:

i and j are locations, and ij is the arc that connects them 🔗.
a_ij, b_ij, and c_ij are parameters specific to each arc (I'll provide these) ⚙️.
x_ij​ is the amount of goods shipped along the arc 📦.
For instance, an arc with a_ij = 6, b_ij = 14, and c_ij = 18 means that sending x units along this arc has a cost:

f(x_ij) = -6x_ij^2 + 14x_ij + 18

So I need to decide:

Which arcs to use 📍
How much to send along each arc 🚛
Can you help me solve this problem? 🧩

Let's minimize the cost while keeping everyone happy!

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7273242794477932545-mmYH?utm_source=share&utm_medium=member_desktop)

# Analysis

The instance file seems incorrect. When I read route cost data from it, there appear to be some loops and also 'dead end' customers.
To fix the issues, I removed the loops and for 'dead end' customers added an outgoing arc for each incoming arc with the same cost.

Here's the resulting network and solution.

There are not so many possible routes, so I coded a depth-first branch and bound search procedure. It
