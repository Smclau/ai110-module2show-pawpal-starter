from pawpal_systems import Owner, Pet, Task, Schedule, Priority
from datetime import date, time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Plan your pet's day with ease. Add tasks, set priorities, and generate a daily schedule tailored to your time and your pet's needs.
"""
)

st.divider()

st.subheader("Owner & Pet Profile")
owner_name = st.text_input("Owner name", value="Jordan")
available_hours = st.number_input("Available hours per day", min_value=1, max_value=24, value=8)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add tasks for your pet's day. They will be used to generate the schedule.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, available_hours)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species, 0)
    st.session_state.owner.add_pet(st.session_state.pet)


if st.button("Create Profile"):
    st.session_state.owner = Owner(owner_name, available_hours)
    st.session_state.pet = Pet(pet_name, species, 0)
    st.session_state.owner.add_pet(st.session_state.pet)
    st.session_state.tasks = []
    st.success(f"Profile created for {owner_name} and {pet_name}!")
    
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.time_input("Time", value=time(8, 0))

if st.button("Add task"):
    new_task = Task(
        task_title,
        int(duration),
        Priority[priority.upper()],
        date.today(),
        task_time
    )
    st.session_state.pet.add_task(new_task)
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    df = pd.DataFrame([{"#": i+1, **t} for i, t in enumerate(st.session_state.tasks)])
    st.dataframe(df.set_index("#"))

    task_to_remove = st.selectbox("Remove task", [t["title"] for t in st.session_state.tasks])
    if st.button("Remove task"):
        st.session_state.pet.rmv_task(task_to_remove)
        st.session_state.tasks = [t for t in st.session_state.tasks if t["title"] != task_to_remove]
        st.success(f"'{task_to_remove}' removed.")

    task_to_complete = st.selectbox("Mark task complete", [t["title"] for t in st.session_state.tasks])
    if st.button("Mark complete"):
        for task in st.session_state.pet.tasks:
            if task.task_name == task_to_complete:
                task.mark_complete()
        st.session_state.tasks = [
            {**t, "status": "Complete"} if t["title"] == task_to_complete else t
            for t in st.session_state.tasks
        ]
        st.success(f"'{task_to_complete}' marked complete!")
else:
    st.info("No tasks yet. Add one above.")

st.divider()
st.subheader("Build Schedule")

if st.button("Generate Schedule"): 
    owner = st.session_state.owner
    pet = st.session_state.pet

    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    st.text(schedule.show_schedule())
