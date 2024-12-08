# P5: Best locations

## 🧠 The problem

Hi, FlORence ici 🇫🇷

I'm a manager of AmazOR that wants to find the best possible locations for our warehouses while deciding how to allocate our client demands to these warehouses.

Our warehouses can only handle a limited amount of demand but we need to ensure that all client demands are met.

While opening a new facility, we have some fixed costs, and we also take into account the cost of allocating the demand of each client to each warehouse.

Of course, we want to minimize our costs here...

Can you help me solve this problem?

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7270343693419597824-FTpE?utm_source=share&utm_medium=member_desktop)

## Analysis

The decisions include opening the warehouses, and assigning the customers to each warehouse. Both are binary.

The constraints:

- The assigned demand not exceeds the capacity of the warehouse

- Assignments are only allowed to the opened warehouses

- Each customer must be allocated to a warehouse

The objective:
Minimize total fixed cost + total allocation cost

_Update:_
The model can't be solved with the constraint to use just one warehouse for allocation. Some customers have demand too large for any warehouse.
I changed the constraints to allow more than one warehouse for sourcing and replaced the allocation with an additional continuous sourcing variable in the capacity constraints.
For customers, there's a new demand satisfaction constraint, it must source all its demand somewhere.

The problem with continuous variable solves significanlty longer than the pure binary problem.

It might be worth adding one more constraint limiting the number of opened warehouses.
