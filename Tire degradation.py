import time
import sys

# --- 1. DATA ARCHITECTURE ---
TRACK_DB = {
    "Monza": {
        "wear_factor": 0.8, 
        "stress": "Rear (Heavy Traction)", 
        "type": "Low Downforce / High Speed"
    },
    "Silverstone": {
        "wear_factor": 1.4, 
        "stress": "Front-Left (Critical Structural Stress)", 
        "type": "High Speed / High Lateral Load"
    },
    "Singapore": {
        "wear_factor": 1.1, 
        "stress": "Rear (Heavy Traction)", 
        "type": "High Downforce / Street Circuit"
    }
}

BASE_TIRES = {
    "Soft": 22,
    "Medium": 35,
    "Hard": 55
}

# --- 2. TERMINAL EFFECTS ---
def type_text(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def loading_bar(text, duration=1.0):
    sys.stdout.write(text)
    sys.stdout.flush()
    time.sleep(duration)
    print()

# --- 3. SYSTEM BOOT ---
print("="*60)
type_text("[INITIALIZING] TIRE STRATEGY TERMINAL v1.0 ...")
loading_bar("[||||||||||||||||||||] SECURE CONNECTION ESTABLISHED", 1)
print("\n> INGESTING TRACK DATABASE... SUCCESS")
print("> CALIBRATING THERMAL MODELS... SUCCESS")
print("="*60)

# --- 4. VARIABLE INPUTS ---
print("\n--- STRATEGIC INPUT REQUIRED ---")
driver_name = input("> Enter Driver Name: ")
selected_track = input("> Select Circuit [Monza / Silverstone / Singapore]: ").capitalize()
start_tire = input("> Enter Starting Compound [Soft / Medium / Hard]: ").capitalize()
track_temp = input("> Track Temperature [Standard / Scorching]: ").capitalize()
slip_angle = input("> Setup Bias: High Slip Angle (Oversteer) detected? (Y/N): ").upper()
traffic_gap = float(input("> Track Position: Gap to car ahead (in seconds): "))

# Extract track data
track_data = TRACK_DB.get(selected_track, TRACK_DB["Silverstone"]) # Default to Silverstone if typo
base_cliff = int(BASE_TIRES[start_tire] / track_data["wear_factor"])
adjusted_cliff = base_cliff

# --- 5. THE LOGIC MATH ---
print("\n" + "="*60)
type_text("[CALCULATING KINEMATIC DROP-OFF...]", 0.03)

if track_temp == "Scorching":
    loading_bar("[|||||||             ] Applying Scorching Track Penalty (-10% Overall Life)", 0.8)
    adjusted_cliff -= int(base_cliff * 0.10)

if slip_angle == "Y":
    loading_bar("[||||||||||||        ] Applying High Slip Angle Penalty (+12% Rear Wear)", 0.8)
    adjusted_cliff -= int(base_cliff * 0.12)

loading_bar(f"[||||||||||||||||    ] Analyzing Asymmetric Stress (Limiting Tire: {track_data['stress']})", 0.8)
loading_bar("[||||||||||||||||||||] Calculation Complete.", 0.5)

# Calculate Undercut
if traffic_gap <= 1.0:
    pit_lap = adjusted_cliff - 3 # Pit 3 laps early to jump the car ahead
    undercut_status = True
else:
    pit_lap = adjusted_cliff - 1
    undercut_status = False

# --- 6. PRIMARY PROTOCOL OUTPUT ---
print("\n>> PRIMARY STRATEGY PROTOCOL <<")
print(f"Circuit: {selected_track.upper()} ({track_data['type']})")
print(f"Limiting Tire: {track_data['stress']}\n")

print(f"Base Tire Cliff: Lap {base_cliff}")
print(f"Adjusted Cliff (Temp + Slip Penalties): Lap {adjusted_cliff}\n")

if undercut_status:
    print("[TRAFFIC ANALYSIS]: Target is within 1.0s (DRS Window).")
    print("[DECISION]: INITIATE AGGRESSIVE UNDERCUT.")
    print(f"BOX ON LAP {pit_lap} FOR HARD COMPOUND. Target clear air on exit.")
else:
    print("[TRAFFIC ANALYSIS]: Target outside DRS Window. Clean air secured.")
    print(f"[DECISION]: STANDARD PIT PROTOCOL. BOX ON LAP {pit_lap} FOR HARD COMPOUND.")

# --- 7. SECONDARY PROTOCOL (CRISIS) ---
print("\n--- SECONDARY STRATEGY PROTOCOL ---")
override = input("> INITIATE CRISIS OVERRIDE? (Y/N): ").upper()

if override == "Y":
    crisis = input("> Enter Crisis Event [Traffic / Rain / RedFlag]: ").capitalize()
    if crisis == "Rain":
        rain_laps = input("> Predicted Laps until Rain: ")
        print("\n[RECALCULATING WEATHER DELTA...]")
        time.sleep(1)
        print(f"[DECISION - PLAN B]: Precipitation imminent before Hard compound temperature window opens.")
        print(f"ABORT LAP {pit_lap} STOP. Extend stint. Bleed pace and survive until Inters window.")

# --- 8. MEDIA BRIEFING ---
print("\n--- MEDIA DEPT. TRANSLATION BRIEF ---")
temp_text = "Scorching track temperatures and high" if track_temp == "Scorching" else "High"
strategy_text = "running an aggressive undercut strategy to jump into clean air" if undercut_status else "running a standard primary strategy"
weather_text = "Rain threatening." if override == "Y" else "Conditions stable."

print(f"{temp_text} degradation at {selected_track} today, especially on the {track_data['stress']}. "
      f"{driver_name} is {strategy_text} and secure track position. {weather_text}")
print("="*60)