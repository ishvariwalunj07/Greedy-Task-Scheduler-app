# Greedy-Task-Scheduler-app

⏱️ Greedy Task Scheduler
This project implements a Greedy Task Scheduler using the Earliest Deadline First (EDF) greedy algorithm to minimize maximum lateness. It provides an interactive Streamlit web app that allows users to input tasks manually or upload a CSV file, and then schedules them optimally.

🔹 Features
📌 Two input methods:
Manual input of tasks
Upload CSV file with TaskName, ProcessingTime, and Deadline

🖥️ Interactive UI built with Streamlit
Collapsible sections for step-by-step task entry
Sidebar for configuration
Tabs for results (Task Table, Gantt Chart, Insights)

📊 Visualizations
Gantt Chart showing scheduled tasks and deadlines
Lateness distribution bar chart

📈 Insights Dashboard
Maximum lateness
Total number of tasks
Total completion time

🔹 Algorithm
The scheduler follows the Earliest Deadline First (EDF) greedy approach:
Sort tasks by their deadlines.
Execute them in order.
Track lateness (finish_time - deadline).
Output schedule with minimized maximum lateness.

🔹 Tech Stack
Python
Streamlit (for web app)
Pandas (for data handling)
Matplotlib (for Gantt Chart visualization)

🔹 Applications
✅ Project scheduling in operations research
✅ Real-time task scheduling in operating systems
✅ Deadline management in project workflows

 This project demonstrates how greedy algorithms can be applied to real-world scheduling problems with a user-friendly interface.
