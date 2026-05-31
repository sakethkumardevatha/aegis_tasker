import json
import os

DB_FILE = "roadmap.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def complete_mission_logic(territory_id, mission_index):
    """Marks a mission complete, adds XP, checks for level ups, and unlocks boss/new lands."""
    data = load_data()
    
    if territory_id in data.get("territories", {}):
        territory = data["territories"][territory_id]
        missions = territory.get("missions", [])
        
        if 0 <= mission_index < len(missions) and missions[mission_index]["status"] == "pending":
            # 1. Complete Mission
            missions[mission_index]["status"] = "done"
            xp_earned = missions[mission_index]["xp_reward"]
            
            # 2. Distribute XP & Process Level Up
            stats = data.get("player_stats", {"level": 1, "current_xp": 0, "next_level_xp": 100, "title": "Novice"})
            stats["current_xp"] += xp_earned
            
            while stats["current_xp"] >= stats["next_level_xp"]:
                stats["current_xp"] -= stats["next_level_xp"]
                stats["level"] += 1
                stats["next_level_xp"] = int(stats["next_level_xp"] * 1.5)
                # Update titles based on milestones
                if stats["level"] >= 5: stats["title"] = "Generative Architect"
                elif stats["level"] >= 3: stats["title"] = "Backend Vanguard"
            
            data["player_stats"] = stats
            
            # 3. Dynamic Map Phase Checking: Unlock the Boss Battle if standard missions are clear
            all_scouting_done = all(m["status"] == "done" for m in missions if m["type"] == "Scouting Mission")
            if all_scouting_done:
                for m in missions:
                    if m["type"] == "Boss Battle" and m["status"] == "locked":
                        m["status"] = "pending"
            
            # 4. Check if whole territory is conquered to unlock next phase
            if all(m["status"] == "done" for m in missions):
                sorted_keys = sorted(data["territories"].keys())
                current_idx = sorted_keys.index(territory_id)
                if current_idx + 1 < len(sorted_keys):
                    next_territory_key = sorted_keys[current_idx + 1]
                    if data["territories"][next_territory_key]["status"] == "locked":
                        data["territories"][next_territory_key]["status"] = "unlocked"
            
            save_data(data)
            return True, xp_earned
            
    return False, 0

def add_side_quest(quest_text, xp_reward=20):
    data = load_data()
    quest = {
        "id": f"side_{int(os.getpid())}",
        "type": "Side Quest",
        "objective": quest_text,
        "xp_reward": xp_reward,
        "status": "pending"
    }
    if "side_quests" not in data:
        data["side_quests"] = []
    data["side_quests"].append(quest)
    save_data(data)

def complete_side_quest_logic(quest_index):
    data = load_data()
    quests = data.get("side_quests", [])
    if 0 <= quest_index < len(quests) and quests[quest_index]["status"] == "pending":
        quests[quest_index]["status"] = "done"
        xp_earned = quests[quest_index]["xp_reward"]
        
        stats = data.get("player_stats", {"level": 1, "current_xp": 0, "next_level_xp": 100, "title": "Novice"})
        stats["current_xp"] += xp_earned
        
        while stats["current_xp"] >= stats["next_level_xp"]:
            stats["current_xp"] -= stats["next_level_xp"]
            stats["level"] += 1
            stats["next_level_xp"] = int(stats["next_level_xp"] * 1.5)
            
        data["player_stats"] = stats
        save_data(data)
        return True, xp_earned
    return False, 0