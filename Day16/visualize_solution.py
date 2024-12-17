import matplotlib.pyplot as plt
import pandas as pd
import os

# Read data from the file
os.chdir('Day16')
file_path = 'solution.txt'


# Read data from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Find the starting line for tasks
start_marker = "Tasks assignment to crews [task, start, end, team]"
task_start_idx = 0
for idx, line in enumerate(lines):
    if line.strip() == start_marker:
        task_start_idx = idx + 1
        break

# Parse the tasks from the file
tasks = []
for line in lines[task_start_idx:]:
    if line.strip():  # Check if the line is not empty
        parts = line.strip().split()
        if parts[0].isdigit():  # Check if the line starts with a task ID (a digit)
            task_id, start, end, team = map(int, parts)
            tasks.append({'Task': task_id, 'Start': start,
                         'End': end, 'Team': team})

# Convert tasks to a DataFrame
data = pd.DataFrame(tasks)

# Create a Gantt chart
plt.figure(figsize=(16, 16))  # Make the chart wider and shorter

# Generate colors for each team
teams = data['Team'].unique()
team_colors = {team: f'C{idx % 10}' for idx, team in enumerate(teams)}

for _, task in data.iterrows():
    bar = plt.barh(y=task['Team'], width=task['End'] - task['Start'],
                   left=task['Start'], color=team_colors[task['Team']], edgecolor='black')
    plt.text(x=task['Start'] + (task['End'] - task['Start']) / 2, y=task['Team'], s=str(task['Task']),
             va='center', ha='center', color='white', fontsize=8)  # Add task numbers

# Configure plot
y_ticks = sorted(data['Team'].unique())
plt.yticks(y_ticks, [f'Team {team}' for team in y_ticks])
plt.xlabel('Time')
plt.ylabel('Teams')
plt.title('Gantt Chart of Task Assignments')
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Save the plot to a file
plt.savefig('schedule.png')
