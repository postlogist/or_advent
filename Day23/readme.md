View in browser

P23: diversify

## 🧠 The problem

Hi again! 👋

Our company is launching a new product line! 🎉

To ensure we cater to the broadest range of customer preferences, we must select 6 products from a pool of 30 candidates.

📊 The chosen products should be as diverse as possible, such that the smallest difference between any two products is maximized.

Considering we know the distances between products...

How can we achieve the most distinct set of products for our launch?

Can you help me solve this problem? 🧩

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7276892581949509633-EYmW?utm_source=share&utm_medium=member_desktop)

## Analysis

Variable:

- We need binaries for product choice and an auxiliary var for min distance between selected products

Objective:
maximize min_distance
Constraints:

- The number of products selected
- A constraint to link min_distance and product choice

## Results

'''
Solving instance: instance

Maximum min distance: 152.9
Products selected:
4, min distance: 152.9
5, min distance: 164.9
14, min distance: 164.4
20, min distance: 156.4
26, min distance: 154.6
29, min distance: 152.9
'''
