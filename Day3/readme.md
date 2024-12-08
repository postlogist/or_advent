# P3: Assigning tasks

## The problem

Hey, ORville here 👋

I'm a logistics manager overseeing the allocation of tasks to employees in our company, FurnitORe.

Right now we have 100 tasks that need to be completed, and we also have 100 employees available to handle them.

The catch is that assigning a task to an employee has a cost 💸.

These costs vary depending on the difficulty of the task, the expertise of the employee, and other factors.

I need your help to figure out the most cost-effective way to assign these tasks to employees.

You can assume that each task is done by just one employee, and one employee is assigned to just one task.

Can you help me solve this problem?

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7269618917482909696-qJ_2?utm_source=share&utm_medium=member_desktop)

## Analysis

Seems like a classical assignment problem.

The decision variables are binary variables linking an employee to a task. The number of variables is N_e x N_t.

The objective is to minimize the total cost of assignments.

The constraints are: each employee can be assigned to one task only. Each task can be assigned to one employee only.

Interestingly, using just one constraint doesn't produce the correct result.
