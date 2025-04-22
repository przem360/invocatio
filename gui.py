import tkinter as tk
import random
import sys

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

def perform_sacrifices(sacrifice_count):
    state["sacrifices"] = sacrifice_count
    state["population"] -= sacrifice_count
    state["favor"] += sacrifice_count * 3
    state["fear"] += sacrifice_count * 2
    state["cult_power"] += sacrifice_count
    print(f"🩸 {sacrifice_count} sacrificed. Favor +{sacrifice_count*3}, Fear +{sacrifice_count*2}, Cult Power +{sacrifice_count}")

def choose_action(action):
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

def trigger_event(event_choice):
    event = random.choice(events)
    event_text.set(event["text"])
    
    for i, option in enumerate(event["options"]):
        event_buttons[i].config(text=option["label"], command=lambda i=i: on_event_submit(i))

    return event

# --- UI UPDATE FUNCTIONS ---
def update_game_state():
    state_label.config(text=f"Turn {state['turn']}/12\nYear {state['year']} - {state['month']}\n"
                           f"Population: {state['population']} | Faith: {state['faith']} | Fear: {state['fear']}\n"
                           f"Favor: {state['favor']} | Food: {state['stored_food']} | Ritual Materials: {state['ritual_materials']}\n"
                           f"Cult Power: {state['cult_power']} | Insight: {state['insight']}")

def on_sacrifice_submit():
    global sacrifice_entry  # Ensure the entry field is referenced globally
    try:
        sacrifice_count = int(sacrifice_entry.get())
        sacrifice_count = max(0, min(sacrifice_count, state["population"]))
        perform_sacrifices(sacrifice_count)
        sacrifice_frame.pack_forget()
        action_frame.pack()
        update_game_state()
    except ValueError:
        pass

def on_action_submit(action_choice):
    choose_action(action_choice)
    action_frame.pack_forget()
    event_frame.pack()
    event = trigger_event(0)
    update_game_state()

def on_event_submit(option_choice):
    event = trigger_event(0)  # Example of calling event function
    apply_effects(event["options"][option_choice]["effects"])
    event_frame.pack_forget()
    risk_frame.pack()
    update_game_state()

def on_risk_submit():
    check_risk()
    state["cult_power"] = max(0, state["cult_power"] - 1)
    state["turn"] += 1
    if state["turn"] > 12:
        end_game()  # After 12 turns, end the game and display the summary
    else:
        risk_frame.pack_forget()
        update_game_state()
        sacrifice_frame.pack()  # Show sacrifice frame for next turn

# --- MAIN LOOP ---
def start_game():
    global event_text, event_buttons, state_label, action_frame, event_frame, risk_frame, sacrifice_frame, sacrifice_entry

    root = tk.Tk()
    root.title("Invocatio Game")
    root.geometry("600x600")

    # --- UI ELEMENTS ---
    state_label = tk.Label(root, text="", font=("Helvetica", 14))
    state_label.pack()

    food_label = tk.Label(root, text="", font=("Helvetica", 12))
    food_label.pack()

    # --- SACRIFICES FRAME ---
    sacrifice_frame = tk.Frame(root)
    sacrifice_label = tk.Label(sacrifice_frame, text="How many people do you want to sacrifice?")
    sacrifice_label.pack()
    sacrifice_entry = tk.Entry(sacrifice_frame)
    sacrifice_entry.pack()
    sacrifice_button = tk.Button(sacrifice_frame, text="Submit", command=on_sacrifice_submit)
    sacrifice_button.pack()
    sacrifice_frame.pack()

    # --- ACTION FRAME ---
    action_frame = tk.Frame(root)
    action_label = tk.Label(action_frame, text="Choose an action:")
    action_label.pack()
    action_buttons = [
        tk.Button(action_frame, text="Gather food (+50 food)", command=lambda: on_action_submit(1)),
        tk.Button(action_frame, text="Search for ritual materials (+1 material)", command=lambda: on_action_submit(2)),
        tk.Button(action_frame, text="Knowledge ritual (+1 insight, -1 material)", command=lambda: on_action_submit(3)),
        tk.Button(action_frame, text="Power ritual (+5 favor, -2 materials)", command=lambda: on_action_submit(4)),
    ]
    for button in action_buttons:
        button.pack()

    # --- EVENT FRAME ---
    event_frame = tk.Frame(root)
    event_text = tk.StringVar()  # Variable to hold the event description text
    event_label = tk.Label(event_frame, textvariable=event_text, wraplength=450)
    event_label.pack()
    event_buttons = [
        tk.Button(event_frame, text="", command=lambda: on_event_submit(0)),
        tk.Button(event_frame, text="", command=lambda: on_event_submit(1)),
        tk.Button(event_frame, text="", command=lambda: on_event_submit(2)),
    ]
    for button in event_buttons:
        button.pack()

    # --- RISK FRAME ---
    risk_frame = tk.Frame(root)
    risk_label = tk.Label(risk_frame, text="Risk check")
    risk_label.pack()
    risk_button = tk.Button(risk_frame, text="Check risk", command=on_risk_submit)
    risk_button.pack()

    # Start the game
    update_game_state()
    
    # Trigger the first event when the game starts
    trigger_event(0)  # Trigger an event immediately upon starting the game
    
    root.mainloop()

start_game()
