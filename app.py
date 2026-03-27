from pawpal_systems import Owner, Pet, Task, Schedule, Priority, RecurFrequency
from datetime import date, time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("Plan your pet's day with ease. Add tasks, set priorities, and generate a daily schedule tailored to your time and your pet's needs.")

st.divider()

# --- Profile ---
st.subheader("Owner & Pet Profile")
owner_name = st.text_input("Owner name", value="Jordan")
available_hours = st.number_input("Available hours per day", min_value=1, max_value=24, value=8)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, available_hours)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species, 0)
    st.session_state.owner.add_pet(st.session_state.pet)

if st.button("Create Profile"):
    st.session_state.owner = Owner(owner_name, available_hours)
    st.session_state.pet = Pet(pet_name, species, 0)
    st.session_state.owner.add_pet(st.session_state.pet)
    st.success(f"Profile created for {owner_name} and {pet_name}!")

# --- Add Task ---
st.markdown("### Tasks")
st.caption("Add tasks for your pet's day. They will be used to generate the schedule.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.time_input("Time", value=time(8, 0))

recur = st.selectbox("Repeats", ["none", "daily", "weekly"])

PRIORITY_EMOJI = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}

if st.button("Add task"):
    recur_map = {
        "none": RecurFrequency.NONE,
        "daily": RecurFrequency.DAILY,
        "weekly": RecurFrequency.WEEKLY,
    }
    new_task = Task(
        task_title,
        int(duration),
        Priority[priority.upper()],
        date.today(),
        task_time,
        recur=recur_map[recur]
    )
    st.session_state.pet.add_task(new_task)
    st.success(f"'{task_title}' added.")

# --- Task List (single source of truth: pet.tasks) ---
pet = st.session_state.pet

if pet.tasks:
    overdue = pet.get_tasks_by_status("overdue")
    if overdue:
        st.warning(f"{len(overdue)} overdue task(s): {', '.join(t.task_name for t in overdue)}")

    status_filter = st.selectbox("Filter by status", ["all", "pending", "complete", "overdue"])
    filtered = pet.get_tasks_by_status(status_filter) if status_filter != "all" else pet.tasks

    st.write("Current tasks:")
    if filtered:
        rows = [
            {
                "#": i + 1,
                "title": t.task_name,
                "time": t.time.strftime("%I:%M %p") if t.time else "Flexible",
                "duration (min)": t.duration_minutes,
                "priority": f"{PRIORITY_EMOJI[t.priority.name]} {t.priority.name.lower()}",
                "repeats": t.recur.name.lower() if t.recur != RecurFrequency.NONE else "—",
                "status": "Complete" if t.complete else "Pending",
            }
            for i, t in enumerate(filtered)
        ]
        st.dataframe(pd.DataFrame(rows).set_index("#"))
    else:
        st.info(f"No {status_filter} tasks.")

    # Remove task
    task_to_remove = st.selectbox("Remove task", [t.task_name for t in pet.tasks])
    if st.button("Remove task"):
        pet.rmv_task(task_to_remove)
        st.success(f"'{task_to_remove}' removed.")

    # Mark complete — only show pending tasks
    pending_tasks = pet.get_tasks_by_status("pending")
    if pending_tasks:
        task_to_complete = st.selectbox("Mark task complete", [t.task_name for t in pending_tasks])
        if st.button("Mark complete"):
            for task in list(pet.tasks):
                if task.task_name == task_to_complete and not task.complete:
                    task.mark_complete()
                    next_task = task.create_next_occurrence()
                    if next_task:
                        pet.add_task(next_task)
                        st.info(f"'{task_to_complete}' repeats {task.recur.name.lower()} — next occurrence added for {next_task.due}.")
                    break
            st.success(f"'{task_to_complete}' marked complete!")
    else:
        st.success("All tasks complete for today!")

else:
    st.info("No tasks yet. Add one above.")

# --- Schedule ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    owner = st.session_state.owner

    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    schedule.sort_scheduled_by_time()

    for warning in schedule.conflict_warnings():
        st.warning(warning)

    if schedule.scheduled_tasks:
        pending_count = sum(1 for t in schedule.scheduled_tasks if not t.complete)
        st.success(f"Scheduled {len(schedule.scheduled_tasks)} task(s) for {pet.pet_name} — {pending_count} still pending.")
        rows = [
            {
                "Task": t.task_name,
                "Time": t.time.strftime("%I:%M %p") if t.time else "Flexible",
                "Duration": f"{t.duration_minutes} min",
                "Priority": f"{PRIORITY_EMOJI[t.priority.name]} {t.priority.name}",
                "Repeats": t.recur.name.lower() if t.recur != RecurFrequency.NONE else "—",
                "Status": "Complete" if t.complete else "Pending",
            }
            for t in schedule.scheduled_tasks
        ]
        st.table(pd.DataFrame(rows))
    else:
        st.info("No tasks were scheduled.")

    if schedule.overflow_tasks:
        st.warning(f"{len(schedule.overflow_tasks)} task(s) couldn't fit in your available time:")
        for t in schedule.overflow_tasks:
            st.markdown(f"- **{t.task_name}** — {t.duration_minutes} min ({t.priority.name})")
