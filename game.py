import random
import sys

# --- STAN GRY ---
state = {
    "turn": 1,
    "year": 1921,
    "month": "Luty",
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

# --- ZDARZENIA ---
events = [
    {
        "text": "Dziecko wpływowego gospodarza zniknęło. Mieszkańcy podejrzewają kult.",
        "options": [
            {"label": "Poświęć innego wieśniaka jako kozła ofiarnego.", "effects": {"fear": -10, "faith": -5, "population": -1}},
            {"label": "Złóż dziecko w ofierze.", "effects": {"favor": +15, "fear": +15, "population": -1}},
            {"label": "Zignoruj sytuację.", "effects": {"fear": +10}},
        ]
    },
    {
        "text": "Obdartus twierdzi, że słyszy głos z Głębi i chce dołączyć do kultu.",
        "options": [
            {"label": "Przyjmij go i wtajemnicz.", "effects": {"faith": +10}},
            {"label": "Złóż go w ofierze.", "effects": {"favor": +10, "fear": +5}},
            {"label": "Wyrzuć go z miasta.", "effects": {}},
        ]
    },
    {
        "text": "Na murze pojawia się cień w kształcie oka. Mieszkańcy boją się.",
        "options": [
            {"label": "Ogłoś cud i zrób święto.", "effects": {"faith": +15, "stored_food": -30}},
            {"label": "Rytuał objaśnienia.", "effects": {"favor": +10, "fear": +5}},
            {"label": "Zamaluj cień.", "effects": {"fear": -10, "faith": -10}},
        ]
    },
]

# --- FUNKCJE ---
def apply_effects(effects):
    for key, value in effects.items():
        state[key] = max(0, state.get(key, 0) + value)

def check_risk():
    if state["fear"] >= 80 and state["faith"] <= 30:
        print("\n⚠️ Mieszkańcy są bliscy buntu!")
    if state["fear"] >= 100:
        print("\n🔥 BUNT! Lud powstaje i zrywa się przeciw kultowi!")
        print("💀 KONIEC: Zginąłeś z rąk ludzi.")
        sys.exit()

def end_game():
    print("\n🔚 KONIEC GRY – Rok 1922")
    favor = state["favor"]
    faith = state["faith"]
    fear = state["fear"]

    if favor > 95 and fear > 90:
        print("🤯 Zeszli... Ale nie tak, jak chciałeś. Twój umysł nie wytrzymał.")
    elif favor > 80 and faith > 70 and fear < 50:
        print("🌑 Zejście Głębi nastąpiło. Kult triumfuje.")
    elif favor > 50 and fear < 60:
        print("🕯️ Cisza Po Drugiej Stronie. Przetrwałeś. Ale nie wiesz, czy warto było.")
    else:
        print("🔥 Zguba Miasta. Nie byłeś godny.")
    sys.exit()

# --- GŁÓWNA PĘTLA ---
while state["turn"] <= 12:
    print(f"\n🌘 Miasteczko Ashridge – Tura {state['turn']}/12")
    print(f"Ludność: {state['population']} | Wiara: {state['faith']} | Strach: {state['fear']} | Przychylność: {state['favor']}")
    print(f"Jedzenie: {state['stored_food']} | Materiały rytualne: {state['ritual_materials']} | Moc Kultu: {state['cult_power']} | Wgląd: {state['insight']}")

    # Żywienie
    consumed = state["population"] * 2
    state["stored_food"] -= consumed
    print(f"🍽️ Zużyto {consumed} jedzenia na wykarmienie ludności.")
    if state["stored_food"] < 0:
        print("⚠️ Brakuje jedzenia! Ludzie głodują, wiara spada!")
        state["faith"] = max(0, state["faith"] - 10)
        state["fear"] += 10
        state["population"] = max(0, state["population"] - 5)
        state["stored_food"] = 0

    try:
        s = int(input("👁️  Ilu ludzi chcesz złożyć w ofierze w tym miesiącu? (0–10): "))
        s = max(0, min(s, 10, state["population"]))
    except ValueError:
        s = 0

    state["sacrifices"] = s
    state["population"] -= s
    state["favor"] += s * 3
    state["fear"] += s * 2
    state["cult_power"] += s

    print(f"🩸 Złożono {s} ludzi. Przychylność +{s*3}, Strach +{s*2}, Moc Kultu +{s}")

    print("\n⚙️ Wybierz dodatkową akcję:")
    print("  1. Zbieraj jedzenie (+50 jedzenia)")
    print("  2. Szukaj materiałów rytualnych (+1 materiał)")
    print("  3. Rytuał wiedzy (+1 wgląd, -1 materiał)")
    print("  4. Rytuał mocy (+5 przychylności, -2 materiały)")

    try:
        action = int(input("Twój wybór: "))
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

    # WYDARZENIE
    event = random.choice(events)
    print("\n📜 Wydarzenie:", event["text"])
    for i, opt in enumerate(event["options"]):
        print(f"  {i+1}. {opt['label']}")

    try:
        choice = int(input("Twój wybór: ")) - 1
        if 0 <= choice < len(event["options"]):
            apply_effects(event["options"][choice]["effects"])
    except ValueError:
        pass

    check_risk()
    state["cult_power"] = max(0, state["cult_power"] - 1)
    state["turn"] += 1

end_game()
