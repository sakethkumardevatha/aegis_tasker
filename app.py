import streamlit as st
import json
import os
import time
from database import load_data, save_data, update_task_status, update_task_details, delete_task
from agent_logic import classify_task_with_ai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Aegis OS | AI Engineer Tracker",
    page_icon="🛡️",
    layout="wide"
)

# --- DATA INITIALIZATION ---
data = load_data()

# --- HELPER FUNCTIONS ---
def calculate_metrics(data):
    total = 0
    done = 0
    for day_id in data:
        tasks = data[day_id].get("tasks", [])
        for task in tasks:
            total += 1
            if task.get("status") == "done":
                done += 1
    return done, total

# --- SIDEBAR: GLOBAL PROGRESS ---
st.sidebar.title("🛡️ Aegis OS")
st.sidebar.caption("90-Day AI Engineering Grind")

done_count, total_count = calculate_metrics(data)

if total_count > 0:
    progress_val = done_count / total_count
    st.sidebar.metric("Global Progress", f"{int(progress_val * 100)}%", f"{done_count}/{total_count} Tasks")
    st.sidebar.progress(progress_val)
else:
    st.sidebar.warning("Roadmap file empty or not found.")

st.sidebar.divider()
day_keys = sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else x)
selected_day = st.sidebar.selectbox("📅 Select Day", day_keys)

# --- MAIN INTERFACE ---
if selected_day:
    day_data = data[selected_day]
    day_tasks = day_data.get('tasks', [])
    
    # Header Section
    col_title, col_stat = st.columns([3, 1])
    with col_title:
        st.title(f"Day {selected_day}: {day_data['focus']}")
        st.write(f"**Date:** {day_data.get('date', 'N/A')}")
    
    with col_stat:
        day_done = sum(1 for t in day_tasks if t['status'] == 'done')
        day_total = len(day_tasks)
        st.metric("Day Progress", f"{day_done}/{day_total}")

    # Edit Mode Toggle
    edit_mode = st.toggle("🔧 Edit Mode", help="Enable to modify descriptions or delete tasks")
    st.divider()

    # --- TASK LIST ---
    for i, task in enumerate(day_tasks):
        with st.container():
            if edit_mode:
                # CRUD: Update & Delete Layout
                c1, c2, c3 = st.columns([2, 3, 1])
                with c1:
                    new_topic = st.text_input("Topic", value=task['topic'], key=f"edit_top_{selected_day}_{i}")
                with c2:
                    new_action = st.text_input("Action", value=task['action'], key=f"edit_act_{selected_day}_{i}")
                with c3:
                    st.write("Actions")
                    sub_col1, sub_col2 = st.columns(2)
                    if sub_col1.button("💾", key=f"save_{selected_day}_{i}", help="Save changes"):
                        update_task_details(selected_day, i, new_topic, new_action)
                        st.toast("Task Updated!")
                        st.rerun()
                    if sub_col2.button("🗑️", key=f"del_{selected_day}_{i}", help="Delete task"):
                        delete_task(selected_day, i)
                        st.toast("Task Deleted")
                        st.rerun()
            else:
                # CRUD: Read & Status Update Layout
                c1, c2, c3 = st.columns([0.5, 4, 1])
                with c1:
                    is_completed = (task['status'] == "done")
                    if st.checkbox("", value=is_completed, key=f"chk_{selected_day}_{i}"):
                        if not is_completed:
                            update_task_status(selected_day, i, "done")
                            st.rerun()
                    else:
                        if is_completed:
                            update_task_status(selected_day, i, "pending")
                            st.rerun()
                
                with c2:
                    emoji = {"DSA": "🔴", "ML Theory": "🔵", "ML Math": "🟢", "Project": "🟣", "Tools": "🟠"}.get(task['subject'], "⚪")
                    st.markdown(f"**{emoji} {task['subject']}**: {task['topic']}")
                    st.caption(f"🎯 {task['action']}")
                
                with c3:
                    if task['status'] == "done":
                        st.success("COMPLETE")
                    else:
                        st.info("PENDING")
        
        st.write("") # Spacing between task rows

    # --- AI AGENT HUB: CREATE ---
    st.divider()
    st.subheader("🤖 Aegis Intelligence: Quick Add")
    
    with st.expander("Add Custom Task via Groq Llama-3"):
        user_input = st.text_input("Describe your task:", placeholder="e.g., Build a vector database indexer")
        
        if st.button("Analyze & Inject"):
            if user_input:
                with st.spinner("Classifying with Groq AI..."):
                    ai_category = classify_task_with_ai(user_input)
                    
                    new_task_obj = {
                        "id": int(time.time()),
                        "time": "Extra",
                        "subject": ai_category,
                        "topic": user_input,
                        "action": "Custom task added via AI Agent.",
                        "status": "pending"
                    }
                    
                    data[selected_day]["tasks"].append(new_task_obj)
                    save_data(data)
                    st.success(f"Task classified as {ai_category} and added!")
                    time.sleep(1)
                    st.rerun()

else:
    st.info("Select a day from the sidebar to view your roadmap.")

st.sidebar.divider()
st.sidebar.caption("Containerized AI Development Environment v1.0")