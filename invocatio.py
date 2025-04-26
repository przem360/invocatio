import random
import sys
import os
import json

TOWN_NAME = "Ashridge"

# --- GAME STATE ---

default_state = {
    "turn": 1,
    "year": 1921,
    "month": "February",
    "population": 120,
    "faith": 35,
    "fear": 15,
    "favor": 20,
    "sacrifices": 0,
    "stored_food": 400,
    "ritual_materials": 3,
    "cult_power": 10,
    "insight": 0,
}

state = default_state.copy()

# --- EVENTS ---

events = [
    {
        "text": "The child of a prominent farmer has disappeared. Villagers suspect the cult.",
        "options": [
            {"label": "Sacrifice another villager as a scapegoat.", "effects": {"fear": -10, "faith": -5, "population": -1}},
            {"label": "Sacrifice the child.", "effects": {"favor": +15, "fear": +15, "population": -1}},
            {"label": "Ignore the situation.", "effects": {"fear": +10}},
        ]
    },
    {
        "text": "A ragged man claims he hears voices from the Depths and wants to join the cult.",
        "options": [
            {"label": "Accept and initiate him.", "effects": {"faith": +10}},
            {"label": "Sacrifice him.", "effects": {"favor": +10, "fear": +5}},
            {"label": "Expel him from the town.", "effects": {}},
        ]
    },
    {
        "text": "A shadow in the shape of an eye appears on the wall. Villagers are frightened.",
        "options": [
            {"label": "Declare a miracle and hold a festival.", "effects": {"faith": +15, "stored_food": -30}},
            {"label": "Perform a clarification ritual.", "effects": {"favor": +10, "fear": +5}},
            {"label": "Paint over the shadow.", "effects": {"fear": -10, "faith": -10}},
        ]
    },
]

# --- GAME SAVE / LOAD ---

def save_state():
    try:
        with open("state.txt", "w") as f:
            json.dump(state, f)
        print("💾 Gra zapisana.")
    except Exception as e:
        print(f"❌ Błąd zapisu gry: {e}")

def load_state():
    global state
    if os.path.exists("state.txt"):
        choice = input("📁 Wykryto zapis gry. Wczytać stan gry? (t/n): ").strip().lower()
        if choice == "t":
            try:
                with open("state.txt", "r") as f:
                    state = json.load(f)
                print("✅ Wczytano zapis gry.")
            except Exception as e:
                print(f"❌ Błąd wczytywania stanu: {e}")
                state = default_state.copy()
        else:
            state = default_state.copy()
    else:
        state = default_state.copy()

# --- CORE FUNCTIONS ---

def apply_effects(effects):
    for key, value in effects.items():
        state[key] = max(0, state.get(key, 0) + value)

def check_risk():
    if state["fear"] >= 80 and state["faith"] <= 30:
        print("\n⚠️ The villagers are on the verge of rebellion!")
    if state["fear"] >= 100:
        print("\n🔥 REBELLION! The people rise up against the cult!")
        print("💀 ENDING: You were killed by the mob.")
        sys.exit()

def end_game():
    print("\n🔚 END OF GAME – Year 1922")
    favor = state["favor"]
    faith = state["faith"]
    fear = state["fear"]

    if favor > 95 and fear > 90:
        print("🤯 They came... but not as you hoped. Your mind couldn’t handle it.")
    elif favor > 80 and faith > 70 and fear < 50:
        print("🌑 The Descent of the Depths has occurred. The cult triumphs.")
    elif favor > 50 and fear < 60:
        print("🕯️ Silence Beyond. You survived. But you're unsure it was worth it.")
    else:
        print("🔥 City’s Doom. You were not worthy.")
    sys.exit()

# --- MODULAR GAME TURN FUNCTIONS ---

def feed_population():
    consumed = state["population"] * 2
    state["stored_food"] -= consumed
    print(f"🍽️ Consumed {consumed} food to feed the population.")
    if state["stored_food"] < 0:
        print("⚠️ Not enough food! People are starving, faith drops!")
        state["faith"] = max(0, state["faith"] - 10)
        state["fear"] += 10
        state["population"] = max(0, state["population"] - 5)
        state["stored_food"] = 0

def perform_sacrifices():
    try:
        s = int(input("👁️  How many people do you want to sacrifice this month? (0–10): "))
        s = max(0, min(s, 10, state["population"]))
    except ValueError:
        s = 0

    state["sacrifices"] = s
    state["population"] -= s
    state["favor"] += s * 3
    state["fear"] += s * 2
    state["cult_power"] += s

    print(f"🩸 {s} sacrificed. Favor +{s*3}, Fear +{s*2}, Cult Power +{s}")

def choose_action():
    print("\n⚙️ Choose an additional action:")
    print("  1. Gather food (+50 food)")
    print("  2. Search for ritual materials (+1 material)")
    print("  3. Knowledge ritual (+1 insight, -1 material)")
    print("  4. Power ritual (+5 favor, -2 materials)")

    try:
        action = int(input("Your choice: "))
        if action == 1:
            state["stored_food"] += 50
        elif action == 2:
            state["ritual_materials"] += 1
        elif action == 3 and state["ritual_materials"] >= 1:
            state["ritual_materials"] -= 1
            state["insight"] += 1
        elif action == 4 and state["ritual_materials"] >= 2:
            state["ritual_materials"] -= 2
            state["favor"] += 5
            state["cult_power"] += 2
    except ValueError:
        pass

def trigger_event():
    event = random.choice(events)
    print("\n📜 Event:", event["text"])
    for i, opt in enumerate(event["options"]):
        print(f"  {i+1}. {opt['label']}")

    try:
        choice = int(input("Your choice: ")) - 1
        if 0 <= choice < len(event["options"]):
            apply_effects(event["options"][choice]["effects"])
    except ValueError:
        pass

# --- MAIN LOOP ---

def main():
    load_state()

    while state["turn"] <= 12:
        print(f"\n🌘 Town of {TOWN_NAME} – Turn {state['turn']}/12")
        print(f"Population: {state['population']} | Faith: {state['faith']} | Fear: {state['fear']} | Favor: {state['favor']}")
        print(f"Food: {state['stored_food']} | Ritual Materials: {state['ritual_materials']} | Cult Power: {state['cult_power']} | Insight: {state['insight']}")

        feed_population()
        perform_sacrifices()
        choose_action()
        trigger_event()

        check_risk()
        state["cult_power"] = max(0, state["cult_power"] - 1)
        save_state()
        state["turn"] += 1

    end_game()

if __name__ == "__main__":
    main()
