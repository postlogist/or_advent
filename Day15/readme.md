# P15: improving marketing

## 🧠 The problem

I'm the marketing manager of WalmORt planning an exciting promotion campaign 🛒

I want to maximize the total profit 💰 from a combination of products featured in a special deal.

🛍️ Key details:

Each product has:
🤑 An individual appeal to customers (profit).
🔗 A cross-sell effect when paired with specific other products (synergy).
Each product also has an individual cost 💸.
The total cost of the selected bundle must not exceed a fixed budget 🧾

Can you help me solve this problem? 🧩

Let’s optimize the product selection and make this campaign a blockbuster! 🚀

link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7273967581286318080-5qsn?utm_source=share&utm_medium=member_desktop)

## Analysis

The decision variables are promo choices for each product

The objective is the sum of the individual effects from the promo, and the synergy effects, when the two products are promoted at the same time

The constraint is the budget for the promo spend.

The tricky part is that the synergy effects require a quadratic terms, since both products i and j must be promoted at the same time. This is a product of the two logical variables.

It's possible to linearize this relationship via logical constraints.
