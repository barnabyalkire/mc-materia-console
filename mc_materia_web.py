
import streamlit as st
import random
from datetime import datetime, timedelta
import os

# ---- Custom CSS for Retro RPG Style ----
custom_css = '''
    <style>
        body {
            background-color: #0c0f13;
            color: #e0e6ed;
        }
        .stApp {
            font-family: 'Courier New', Courier, monospace;
            background-color: #0c0f13;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        h1, h2, h3 {
            color: #7dd3fc;
            text-shadow: 0 0 10px #38bdf8;
        }
        .stProgress > div > div > div {
            background-image: linear-gradient(to right, #38bdf8, #3b82f6);
        }
        .stMarkdown p {
            font-size: 16px;
        }
        .badge {
            font-size: 20px;
            padding: 6px;
            border-radius: 5px;
            background: #1f2937;
            color: #facc15;
            box-shadow: 0 0 10px #facc15;
        }
    </style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Define the materia and their related prompts
materia = {
    "Faith (Blue)": "How did grace show up today—even if it was hard to notice?",
    "Compassion (Green)": "How did you offer yourself softness today?",
    "Resilience (Purple)": "How did you keep going today when quitting whispered to you?",
    "Insight (Yellow)": "How would your thoughts sound if they narrated your day?",
    "Shadow-Walker (Red)": "How did your pain show up today, and what did it try to teach?",
    "Tzadik (Gold)": "How did righteousness live in you today—in thought, speech, or restraint?",
    "Code-Smith (Silver)": "How did you build or shape something real today—even if it was just in your mind?",
    "Love-for-Others (White)": "How did someone else’s struggle move you today?"
}

# Load XP from file or initialize
xp_file = "xp.txt"
if os.path.exists(xp_file):
    with open(xp_file, "r") as file:
        try:
            current_xp = int(file.read())
        except ValueError:
            current_xp = 0
else:
    current_xp = 0

# Load streak from file or initialize
streak_file = "streak.txt"
streak = 0
last_entry_date = None

if os.path.exists(streak_file):
    with open(streak_file, "r") as file:
        data = file.read().split(',')
        if len(data) == 2:
            try:
                streak = int(data[0])
                last_entry_date = datetime.strptime(data[1], "%Y-%m-%d").date()
            except ValueError:
                pass

today = datetime.now().date()
new_day = last_entry_date != today

# Constants for XP bar
level_up_xp = 10
current_level = current_xp // level_up_xp + 1
xp_in_level = current_xp % level_up_xp

# UI: Title and XP
st.title("💾 MATERIA REFLECTION TERMINAL")
st.markdown("🧠 *MindfullyCompassionate Console — Retro RPG Edition*")

st.markdown(f"**Level {current_level}**")
st.progress(xp_in_level / level_up_xp)

# Streak display and badge
badge = ""
if last_entry_date:
    if today - last_entry_date == timedelta(days=1):
        st.success(f"🔥 Daily Streak: {streak} days")
    elif today - last_entry_date > timedelta(days=1):
        st.warning("Streak broken. Start again!")
        streak = 0
else:
    st.info("No streak started yet.")

# Badge icons
if streak >= 1:
    badge = "🏅"
if streak >= 3:
    badge = "🎖️"
if streak >= 7:
    badge = "🌟"

if badge:
    st.markdown(f"<div class='badge'>Daily Reflection Badge: {badge}</div>", unsafe_allow_html=True)

# Materia selection
selected_materia = st.multiselect("Select up to 2 Materia:", list(materia.keys()), max_selections=2)

if selected_materia:
    chosen_prompt = random.choice([materia[m] for m in selected_materia])
    
    st.subheader("🔮 Reflection Prompt")
    st.write(f"**{chosen_prompt}**")
    
    response = st.text_area("Enter your reflection here:")

    if st.button("💾 Submit Reflection"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n[{timestamp}]\nMateria Equipped: {', '.join(selected_materia)}\nPrompt: {chosen_prompt}\nResponse: {response}\n"
        with open("mc_materia_web_journal.txt", "a") as file:
            file.write(entry)

        # Update XP
        current_xp += 1
        with open(xp_file, "w") as file:
            file.write(str(current_xp))

        # Update Streak
        if new_day:
            if last_entry_date == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1
            with open(streak_file, "w") as file:
                file.write(f"{streak},{today.strftime('%Y-%m-%d')}")

        st.success("Reflection saved. XP gained. Materia charged.")
        st.balloons()

# Journal viewer
st.sidebar.title("📜 Journal Viewer")
if st.sidebar.button("Show Journal Entries"):
    st.sidebar.subheader("🗂️ Your Reflections:")
    if os.path.exists("mc_materia_web_journal.txt"):
        with open("mc_materia_web_journal.txt", "r") as file:
            journal_entries = file.read()
            st.sidebar.text_area("Reflection Archive", journal_entries, height=400)
    else:
        st.sidebar.info("No journal entries found.")
