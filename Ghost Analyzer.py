import time
import sys

# --- 1. KINEMATIC TRACK DATABASE ---
PROFILES = {
    "Monza_T1": {
        "name": "MONZA TURN 1 (Heavy Braking)",
        "base_brake": 120,  # meters
        "base_vmin": 78,    # km/h
        "base_throttle": "At Apex",
        "grip_offset_factor": 1.25,  # meters of braking lost per lap of tire age
        "vmin_offset_factor": 0.5,   # km/h of apex speed lost per lap
        "straight_name": "Curva Grande",
        "time_penalty_multiplier": 0.05 # seconds lost per unit of error
    },
    "Silverstone_Copse": {
        "name": "SILVERSTONE COPSE (High-Speed Aero)",
        "base_brake": 25,
        "base_vmin": 265,
        "base_throttle": "Before Apex",
        "grip_offset_factor": 0.8,
        "vmin_offset_factor": 1.5,
        "straight_name": "Maggotts Approach",
        "time_penalty_multiplier": 0.03
    }
}

# --- 2. TERMINAL UTILITIES ---
def type_text(text, speed=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def progress_bar(text, duration=0.6):
    sys.stdout.write(text)
    sys.stdout.flush()
    time.sleep(duration)
    print()

# --- 3. SYSTEM INITIALIZATION ---
print("="*60)
type_text("[INITIALIZING] TELEMETRY GHOST ANALYZER v1.0 ...")
progress_bar("[||||||||||||||||||||] KINEMATIC ENGINE ONLINE", 0.8)

# --- 4. SIMULATOR INPUT CAPTURE ---
print("\n--- SIMULATOR INPUT REQUIRED ---")
raw_profile = input("> Select Corner Profile [Monza_T1 / Silverstone_Copse]: ").strip().lower()
tire_age = int(input("> Enter Tire Age (Laps): "))
driver_brake = int(input("> Braking Point Marker (meters before corner): "))
driver_pressure = int(input("> Peak Brake Pressure (%): "))
driver_vmin = int(input("> Apex V-Min (km/h): "))
driver_throttle = input("> Throttle Application [Before / At / After]: ").strip().capitalize()

# Bulletproof Fallback Logic
if "silverstone" in raw_profile or "copse" in raw_profile:
    corner = PROFILES["Silverstone_Copse"]
else:
    corner = PROFILES["Monza_T1"]

# --- 5. DYNAMIC OFFSETS & MATH LOGIC ---
print("\n" + "="*60)
type_text("[PROCESSING TELEMETRY CORRELATION...]", 0.02)
progress_bar(f"[|||||||             ] Applying Dynamic Grip Offset (Tire Age = {tire_age})", 0.5)
progress_bar("[||||||||||||        ] Cross-Referencing Entry/Exit Deltas", 0.5)
progress_bar("[||||||||||||||||    ] Calculating Area-Under-Curve Time Penalty", 0.5)
progress_bar("[||||||||||||||||||||] Analysis Complete.", 0.3)

# Calculate Adjusted Targets
target_brake = int(corner["base_brake"] + (tire_age * corner["grip_offset_factor"]))
target_vmin = int(corner["base_vmin"] - (tire_age * corner["vmin_offset_factor"]))

# Calculate Deltas
brake_delta = driver_brake - target_brake
vmin_delta = driver_vmin - target_vmin

# Brake Classification
if brake_delta < -15:
    brake_status = "LATE BRAKING"
elif brake_delta > 15:
    brake_status = "EARLY BRAKING"
else:
    brake_status = "OPTIMAL ENTRY"

# V-Min Classification
if vmin_delta < -5:
    vmin_status = "OVERSLOWED"
elif vmin_delta > 5:
    vmin_status = "WASHING WIDE"
else:
    vmin_status = "OPTIMAL APEX"

# --- 6. BEHAVIORAL DIAGNOSTICS & CHAIN REACTION LOGIC ---
diagnosis = ""
action = ""
profile_flag = ""
time_loss = 0.0

if brake_status == "LATE BRAKING" and vmin_status == "OVERSLOWED":
    diagnosis = f"Braking point compromised by {abs(brake_delta)} meters. Late braking saturated the front axle, forcing a missed geometric apex. Chassis rotation was compromised, resulting in a {abs(vmin_delta)} km/h V-Min deficit and delayed throttle application to prevent rear-lockup."
    action = f"Shift braking point back to {target_brake}m to account for tire degradation offset. Prioritize entry stability over late braking."
    profile_flag = "[OVER-DRIVEN ENTRY / V-SHAPE]"
    time_loss = round(abs(vmin_delta) * corner["time_penalty_multiplier"] + (tire_age * 0.01), 2)
    
elif brake_status == "EARLY BRAKING":
    diagnosis = f"Braking point initiated {abs(brake_delta)} meters early. Chassis under-loaded on entry, resulting in coasting phase before apex and wasted entry momentum."
    action = f"Push braking point deeper to {target_brake}m. Trust the aerodynamic platform on entry."
    profile_flag = "[UNDER-DRIVEN ENTRY / U-SHAPE]"
    time_loss = round(abs(brake_delta) * 0.02, 2)
    
else:
    diagnosis = "Kinematic sequence stable. Entry and apex parameters within acceptable operational window."
    action = "Maintain current phase targets. Shift focus to micro-adjusting throttle application out of the corner."
    profile_flag = "[OPTIMAL / BALANCED]"
    time_loss = 0.00

# --- 7. TERMINAL OUTPUT GENERATION ---
print(f"\n>> CORNER DIAGNOSTIC: {corner['name']} <<")
print("Reference Baseline: Ghost Driver (Fresh Softs)")
print(f"Adjusted Target: Ghost Driver ({tire_age}-Lap Degradation Applied)")

print("\n[PHASE 1: ENTRY DYNAMICS]")
print(f"- Target Braking Point : {target_brake}m (Baseline {corner['base_brake']}m + {int(tire_age * corner['grip_offset_factor'])}m grip offset)")
print(f"- Driver Braking Point : {driver_brake}m")
print(f"- Telemetry Delta      : {brake_delta}m ({brake_status})")

print("\n[PHASE 2: APEX KINEMATICS]")
print(f"- Target V-Min         : {target_vmin} km/h")
print(f"- Driver V-Min         : {driver_vmin} km/h")
print(f"- Telemetry Delta      : {vmin_delta} km/h ({vmin_status})")

print("\n[PHASE 3: EXIT TRAJECTORY]")
print(f"- Target Throttle      : {corner['base_throttle']}")
print(f"- Driver Throttle      : {driver_throttle}")

print("\n>> ENGINEERING CORRELATION & DIRECTIVE <<")
print(f"[DIAGNOSIS]: {diagnosis}")
print(f"[DIRECTIVE]: {action}")

print("\n>> LAP TIME PROJECTION <<")
print(f"Estimated Time Loss (Turn 1 to {corner['straight_name']} exit): +{time_loss} seconds")

print("\n>> BEHAVIORAL CLASSIFICATION <<")
print(f"Profile: {profile_flag}")
print("="*60)