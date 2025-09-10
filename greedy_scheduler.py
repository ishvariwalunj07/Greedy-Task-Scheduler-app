import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Greedy Task Scheduler",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Scheduler Logic ----------------
def minimize_max_lateness(tasks):
    tasks_sorted = sorted(tasks, key=lambda x: x[2])  # sort by deadline
    current_time = 0
    schedule = []
    max_lateness = 0
    for name, proc_time, deadline in tasks_sorted:
        start = current_time
        finish = start + proc_time
        lateness = max(0, finish - deadline)
        max_lateness = max(max_lateness, lateness)
        schedule.append((name, start, finish, deadline, lateness))
        current_time = finish
    return schedule, max_lateness

# ---------------- Gantt Chart ----------------
def plot_gantt_chart(schedule):
    fig, ax = plt.subplots(figsize=(10, len(schedule) * 0.7))
    for i, (name, start, finish, deadline, _) in enumerate(schedule):
        ax.barh(i, finish - start, left=start, height=0.5,
                color='#4A90E2', edgecolor='black')
        ax.text(start + (finish - start)/2, i, name, va='center',
                ha='center', color='white', fontsize=10, fontweight='bold')
        ax.axvline(x=deadline, ymin=(i - 0.5) / len(schedule),
                   ymax=(i + 0.5) / len(schedule), color='red',
                   linestyle='--', linewidth=1.5)
    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels([t[0] for t in schedule], fontsize=12)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_title("📊 Task Scheduling Gantt Chart (Deadlines in red)",
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', linestyle=':', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

# ---------------- UI Layout ----------------

st.title("⏱️ Greedy Task Scheduler Dashboard")
st.markdown(
    """
    Welcome to the **Greedy Task Scheduler**!  
    This tool applies the **Earliest Deadline First (EDF)** greedy algorithm  
    to schedule tasks while minimizing maximum lateness.  
    """
)

st.divider()

# Step 1: Choose input method
with st.sidebar:
    st.header("⚙️ Configuration")
    input_method = st.radio("Select Input Method:", ["Manual input", "Upload CSV file"])

tasks = []

# Step 2: Enter tasks
if input_method == "Manual input":
    with st.sidebar:
        n = st.number_input("Number of tasks", min_value=1, max_value=30, value=3)
    st.subheader("📝 Enter Task Details")
    task_inputs = []
    for i in range(n):
        cols = st.columns([2, 2, 2])
        name = cols[0].text_input(f"Task {i+1} Name", value=f"Task{i+1}", key=f"name{i}")
        proc = cols[1].number_input(f"Processing Time", min_value=1, max_value=1000, value=1, key=f"proc{i}")
        dead = cols[2].number_input(f"Deadline", min_value=1, max_value=1000, value=proc, key=f"dead{i}")
        task_inputs.append((name.strip(), proc, dead))
    tasks = task_inputs

else:
    st.subheader("📂 Upload CSV File")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = {'TaskName', 'ProcessingTime', 'Deadline'}
            if required_cols.issubset(df.columns):
                tasks = list(zip(df['TaskName'], df['ProcessingTime'], df['Deadline']))
                st.success(f"✅ Loaded {len(tasks)} tasks successfully!")
                st.dataframe(df)
            else:
                st.error(f"CSV must include columns: {required_cols}")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

# Step 3: Run Scheduler
if tasks:
    st.subheader("🚀 Run Scheduler")
    if st.button("Run Greedy Algorithm"):
        schedule, max_lateness = minimize_max_lateness(tasks)

        # Tabs for better UI
        tab1, tab2, tab3 = st.tabs(["📋 Task Table", "📊 Gantt Chart", "📈 Insights"])

        with tab1:
            st.subheader("📋 Scheduled Tasks")
            df_sched = pd.DataFrame(schedule, columns=["Task", "Start", "Finish", "Deadline", "Lateness"])
            st.dataframe(df_sched.style.format({"Start": "{:.0f}", "Finish": "{:.0f}",
                                                "Deadline": "{:.0f}", "Lateness": "{:.0f}"}))

        with tab2:
            plot_gantt_chart(schedule)

        with tab3:
            st.subheader("📈 Key Insights")
            col1, col2, col3 = st.columns(3)
            col1.metric("⚠️ Maximum Lateness", f"{max_lateness}")
            col2.metric("📦 Total Tasks", f"{len(schedule)}")
            col3.metric("⏳ Total Time", f"{schedule[-1][2]}")

            # Show lateness distribution
            lateness_values = [t[4] for t in schedule]
            lateness_df = pd.DataFrame({
                "Task": [t[0] for t in schedule],
                "Lateness": lateness_values
            })
            st.bar_chart(lateness_df.set_index("Task"))

st.markdown("---")
st.markdown("<center><small>✨ Built with Greedy Approach & Streamlit ✨</small></center>", unsafe_allow_html=True)
