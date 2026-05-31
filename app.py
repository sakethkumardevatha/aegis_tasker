import streamlit as st
import time
from database import load_data, save_data, complete_mission_logic, add_side_quest, complete_side_quest_logic
from agent_logic import generate_rpg_side_quest

st.set_page_config(page_title="Aegis Map OS", page_icon="🛡️", layout="wide")

# Read state
data = load_data()
stats = data.get("player_stats", {"level": 1, "current_xp": 0, "next_level_xp": 100, "title": "Novice"})

# --- SIDEBAR: HERO PROFILE ---
st.sidebar.title("🛡️ Hero Profile")
st.sidebar.markdown(f"### **{stats['title']}**")
st.sidebar.metric("Current Level", f"LVL {stats['level']}")

# Level Progress Tracker
progress_percentage = min(1.0, stats["current_xp"] / stats["next_level_xp"])
st.sidebar.progress(progress_percentage)
st.sidebar.caption(f"XP: {stats['current_xp']} / {stats['next_level_xp']} to Next Level")

# Map Directory Processing
territories = data.get("territories", {})
unlocked_territories = {k: v for k, v in territories.items() if v["status"] == "unlocked"}
locked_territories = {k: v for k, v in territories.items() if v["status"] == "locked"}

st.sidebar.divider()
st.sidebar.subheader("🗺️ Map Navigation")
selected_t_id = st.sidebar.selectbox("Travel To:", list(unlocked_territories.keys()), format_func=lambda x: territories[x]["name"])

# --- MAIN WORKSPACE ---
st.title("🗺️ The Realms of Aegis: Quest Tracker")

# 1. Main Unlocked Mission Hub
if selected_t_id:
    t_data = territories[selected_t_id]
    st.header(t_data["name"])
    st.info(f"**Zone Focus:** {t_data['focus']}\n\n*{t_data['description']}*")
    
    st.subheader("🎯 Active Territory Missions")
    
    for i, mission in enumerate(t_data.get("missions", [])):
        with st.container():
            col_box, col_txt, col_badge = st.columns([0.4, 4.5, 1.2])
            
            with col_box:
                m_status = mission["status"]
                if m_status == "done":
                    st.write("✅")
                elif m_status == "locked":
                    st.write("🔒")
                else:
                    if st.checkbox("", key=f"mis_{selected_t_id}_{i}"):
                        success, xp = complete_mission_logic(selected_t_id, i)
                        if success:
                            st.toast(f"Objective Accomplished! +{xp} XP Earned")
                            time.sleep(0.5)
                            st.rerun()
            
            with col_txt:
                type_emoji = "⚔️" if mission["type"] == "Boss Battle" else "🏹"
                st.markdown(f"**{type_emoji} [{mission['type']}] {mission['topic']}**")
                st.write(mission["objective"])
                
            with col_badge:
                if m_status == "done":
                    st.success("CONQUERED")
                elif m_status == "locked":
                    st.caption("Prerequisites Required")
                else:
                    st.warning(f"💎 {mission['xp_reward']} XP")
        st.divider()

# 2. Side Quest Hub (Low Pressure Valve Component)
st.subheader("🎲 Available Side Quests")
active_sides = [q for q in data.get("side_quests", []) if q["status"] == "pending"]

if active_sides:
    for idx, sq in enumerate(data.get("side_quests", [])):
        if sq["status"] == "pending":
            c1, c2, c3 = st.columns([0.5, 4.5, 1])
            with c1:
                if st.checkbox("", key=f"side_chk_{idx}"):
                    success, xp = complete_side_quest_logic(idx)
                    if success:
                        st.toast(f"Side Quest Complete! +{xp} XP")
                        time.sleep(0.5)
                        st.rerun()
            with c2:
                st.markdown(f"**🔹 Mini Mission**")
                st.write(sq["objective"])
            with c3:
                st.info(f"💎 {sq['xp_reward']} XP")
else:
    st.caption("No active side quests in your log. Generate one below if you face a mental roadblock.")

# 3. Dynamic RPG Interaction Layer
with st.expander("🔮 Summon the Game Master"):
    st.write("Brain frozen or feeling stuck? Describe what field is confusing you, and the Game Master will output a 10-minute simple task.")
    input_topic = st.text_input("Enter topic or feeling:", placeholder="e.g., I don't understand container separation")
    
    if st.button("Generate Low-Pressure Task"):
        if input_topic:
            with st.spinner("Formulating directive..."):
                quest_details = generate_rpg_side_quest(input_topic)
                add_side_quest(quest_details)
                st.success("New Quest added to your action log above!")
                time.sleep(1)
                st.rerun()

# 4. Map Display Meta Section (Fog of War Visualization)
if locked_territories:
    st.sidebar.divider()
    st.sidebar.subheader("🌫️ Fog of War (Locked)")
    for lt in locked_territories.values():
        st.sidebar.caption(f"🔒 {lt['name']}")