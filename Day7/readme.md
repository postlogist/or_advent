# P7: logistics everywhere

##🧠 The problem
Hi, DORothy here 🇺🇸

I'm the Chief Operations Officer of OptimizeLogistics, a complex transportation and distribution company from the USA facing a critical optimization challenge.

There are a lot of products that need to be served to our clients, and multiple ways of selecting them.

We usually get several subsets of products, calculate their associated cost (at a subset of products level), and finally select those subsets that minimize our costs.

Of course, all the products must be delivered just once, meaning that a product cannot appear in two different subsets.

I'll give you an example with 135 products and all the 51975 subsets we built with a cost.

Can you help me solve this problem?

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7271068462389628928-WmJa?utm_source=share&utm_medium=member_desktop)

# Analysis

This problem is very similar to the Day 6's problem. The difference is there should be no overlap between different subsets of products, since each product must be delivered once. So it is a set partitioning problem.

I'll try changing the constraint for 'covering' the products to an equality.

...

It solved very quickly to optimality with Total cost: 114852
