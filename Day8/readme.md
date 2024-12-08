# P8: pack

I cannot be happier that you're here, with me, with all your peers in the OR community.

Enjoy and have fun!

## 🧠 The problem

Today I'm the Operations Manager at AmazOR, responsible for efficiently packing items into shipping containers.

I'm always looking for a clear, optimized packing plan to reduce our costs.

The fewer bins we use, the less money we spend on transportation and warehousing.

However, we must be careful not to violate container limits, as overpacked bins can lead to fines or damage.

I'll give you some examples of the issue that we have, considering:

The bin capacity
The number of items to be packed
The number of bins we got in a solution (as a reference for you)
And the size of each item to be packed
Can you help me solve this problem?

Here you can find an instance of this problem.

PS: what strategies would you use to determine which items go into each bin?

PS2: what challenges do you think arise when scaling this problem to thousands of items and multiple bin capacities?

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7271430871214161920-qOxc?utm_source=share&utm_medium=member_desktop)

## Analysis

This is an example of bin packing problem. The decision variables are: the use of bins, and the choice of items for each bin - both binary.

The objective is to minimize the number of bins used.

Since the bins are identical, there's a lot of symmetries in which bin to put the item. I'll try to break some symmetries by allowing to put item i in a bin 1..i;

# Real-world use

1. Using heuristics

The solver sticks when approaching the minimum possible number of bins. It is possible to limit the solution time, and compare the best known MIP solution to the heuristic solution obtained from the First Fit heuristic, choosing the best solution of the two. Alternatively, we could use heuristic solution as a warm start for the MIP solver.

2. When using differently sized boxes, we could use a two-stage approach: first, classify items into large and small. Then pack large items. Then, use the first stage result to pack remaining small items.
