# P22: schedule, please

## 🧠 The problem

Today I'm the Operations Manager in a GigafactORy ⚙️.

🏗️ The scenario:

Our manufacturing plant receives job orders from clients 📝.

Each order consists of multiple tasks, which must:

Be processed on specific machines 🛠️.
Follow a predefined sequence of operations.
⚡ The challenge:

Machines are shared across all tasks, which means:

🔄 Task conflicts can arise when multiple jobs need the same machine at the same time.

⏳ We need an optimized schedule to minimize:

Delays 🕒
Total completion time ✅
🎯 The goal:

To create a production schedule that:

✨ Minimizes the total completion time (makespan).

📋 Respects the sequence of tasks.

⚙️ Avoids machine conflicts between overlapping jobs.

Can you help me solve this problem? 🧩

Here you can find an instance of this problem.

Get the important things from the definition (objective function, constraints, decision variables)
Document your journey
Share your thoughs in my [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7276592031114661888-djFm?utm_source=share&utm_medium=member_desktop) for today (you'll recognize it easily)

## Analysis

I re-purposed the model from P19. It already allowed to change the sequence of jobs at each machine. Now I added the ability to use different machines at each stage.
