# P12: let's serve those orders

## 🧠 The problem

Now it's time to deliver! 🚚

Remember all the orders we received yesterday at the warehouse?

Well... We need to deliver them.

The main problem is that we made a sub-contract for that and there's only one vehicle available... For 443 places to go! 😱

We’ve noticed that going from location A to location B might be different from going from B to A 🔄🚦.

So we need to figure out the best possible path to minimize ⏱️ delivery times.

Can you help me solve this problem? 🧩

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7272880408151666689-SC6Z?utm_source=share&utm_medium=member_desktop)

🎯 Challenge time:
Since this is a well-known problem in the literature, let’s make it a mini competition 🎉:

Submit your solution with:
The value of the Objective Function for your path
Your running time 🕒
A link to your code 💻
I’ll collect all submissions in today’s LinkedIn post, and everything will be summarized on this [Notion page](https://orfrom0to1.bmenendez.com/ty/c/eyJ2Ijoie1wiYVwiOjUyODU2NixcImxcIjoxNDA0NDY2OTA3NTQ2OTIxNjQsXCJyXCI6MTQwNDk5ODI1NjEwMTk2MzUwfSIsInMiOiIyOWQ0MDNjYmM4ZWY2NjZjIn0). I've added modeling language and solver just in case, but if you build a heuristic here I'd write the programming language and the name of the heuristic.
Let's see who rocks it! 🎸

⚠️ Reminder ⚠️

This challenge is about to documenting and sharing so we all can improve the way we think about optimization problems, not about actually solving all the 24 problems in 24 days. Don't feel forced to compete here.

# Solution

Total distance: 2720
Running time: 600 sec for heuristic, 1400 sec for MIP.

I used ortools solver for VRP with Tabu Search first. This produced a solution with objective 2726. Then I used this solution as a warm start for a MIP model with MTZ formulation in AMPL. Highs solved this to optimality in 1400 sec. Not sure, if the warm start actually worked though.
