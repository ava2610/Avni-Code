import time
import sys

# --- 1. CONFIGURATION & SIMULATION DATABASES ---
CIRCUITS = {
    "Monza": {
        "type": "Low Downforce / High Speed",
        "t1_name": "Turn 1 (Rettifilo)",
        "t1_harvest": 12,
        "straight_name": "Curva Grande",
        "t2_name": "Turn 4 (Roggia)",
        "t2_harvest": 5,
        "deploy_corners": "Lesmo 1 & 2 Exits",
        "deploy_amount1": 15,
        "s3_complex": "Ascari Chicane",
        "deploy_amount2": 20,
        "final_corner": "Parabolica",
        "final_harvest": 8
    },
    "Suzuka": {
        "type": "High Downforce / Figure-Eight Circuit",
        "t1_name": "Turn 1 & 2",
        "t1_harvest": 8,
        "straight_name": "S Curves (T3-T7)",
        "t2_name": "The Hairpin (T11)",
        "t2_harvest": 10,
        "deploy_corners": "Spoon Curve Exit",
        "deploy_amount1": 15,
        "s3_complex": "130R Approach",
        "deploy_amount2": 15,
        "final_corner": "Casio Triangle (Chicane)",
        "final_harvest": 12
    },
    "Silverstone": {
        "type": "High Speed / High Lateral Load",
        "t1_name": "Village & The Loop",
        "t1_harvest": 10,
        "straight_name": "Wellington Straight",
        "t2_name": "Brooklands (T6)",
        "t2_harvest": 8,
        "deploy_corners": "Luffield Exit",
        "deploy_amount1": 15,
        "s3_complex": "Maggotts & Becketts Exit",
        "deploy_amount2": 18,
        "final_corner": "Vale Chicane",
        "final_harvest": 10
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
type_text("[INITIALIZING] HYBRID KINETIC DEPLOYMENT MAPPER v3.0 ...")
progress_bar("[||||||||||||||||||||] ERS MODULE ONLINE", 0.8)

# --- 4. TELEMETRY INPUT CAPTURE ---
print("\n--- KINETIC INPUT REQUIRED ---")
selected_circuit = input("> Select Circuit [Monza / Suzuka / Silverstone]: ").capitalize()
engine_mode = input("> Target Engine Mode [Recharge / Balanced / Overtake]: ").capitalize()
initial_soc = int(input("> Current Battery Charge (%): "))
target_gap = float(input("> Track Position: Gap to car ahead (in seconds): "))

# Fallback mechanism for unexpected track typing
if selected_circuit not in CIRCUITS:
    selected_circuit = "Monza"
track = CIRCUITS[selected_circuit]

# --- 5. MODEL PROCESSING RECAPTIONS ---
print("\n" + "="*60)
type_text("[PROCESSING MODEL CONFIGURATION...]", 0.02)
progress_bar("[|||||||             ] Mapping MGU-K Kinetic Harvest Zones", 0.5)
progress_bar("[||||||||||||        ] Mapping 100kW Regulation Derating Ramps", 0.5)
progress_bar("[||||||||||||||||    ] Monitoring 7MJ Energy Cap Compliance", 0.5)
progress_bar("[||||||||||||||||||||] Configuration Complete.", 0.3)

print(f"\n>> HYBRID STRATEGY: {selected_circuit.upper()} ({track['type']}) <<")
print(f"Target Mode: {engine_mode.upper()}")
print(f"Initial SOC: {initial_soc}%")

# --- 6. CORE COMPLIANCE AND TRACKING LOGIC ---
running_soc = initial_soc
total_harvested_mj = 0.0
harvest_cap_triggered = False

# Rule 1: Manual Override Mode (MOM) Check
mom_active = target_gap < 1.0

if mom_active:
    print("\n[PROTOCOL ENGAGED]")
    print("Delta to target < 1.0s. Manual Override Mode (MOM) Active.")
    print("+0.5MJ allocation applied to ERS-K deployment curve.")
else:
    print("\n[PROTOCOL: STANDARD RUNNING]")
    print("Delta to target >= 1.0s. Standard ERS mapping tracking profiles.")

def process_harvest(base_gain):
    global total_harvested_mj, harvest_cap_triggered
    mj_gain = base_gain * 0.58 
    
    if harvest_cap_triggered:
        return 0
    
    if (total_harvested_mj + mj_gain) >= 7.0:
        harvest_cap_triggered = True
        allowed_mj = 7.0 - total_harvested_mj
        total_harvested_mj = 7.0
        allowed_soc_fraction = int(allowed_mj / 0.58)
        return allowed_soc_fraction
    else:
        total_harvested_mj += mj_gain
        return base_gain

# --- 7. DYNAMIC CORNER-BY-CORNER SIMULATION EXECUTION ---
print("\n[SECTOR 1]")
gained = process_harvest(track['t1_harvest'])
running_soc += gained
print(f"- {track['t1_name']}: MGU-K MAX HARVEST. (+{gained}% SOC)")

if mom_active and engine_mode == "Overtake":
    running_soc -= 20
    print(f"- {track['straight_name']}: MOM DEPLOY. Constant 350kW output. (-20% SOC)")
else:
    print(f"- {track['straight_name']}: HOLD. Deployment inhibited via Aero Drag optimization. (0% SOC)")

print("\n[SECTOR 2]")
if engine_mode == "Overtake" or mom_active:
    print(f"- {track['t2_name']} Approach: [DERATING] 100kW ramp-down active (-50m window).")
else:
    print(f"- {track['t2_name']} Approach: Coast profiling linear synchronization active.")

gained = process_harvest(track['t2_harvest'])
running_soc += gained
print(f"- {track['t2_name']}: MGU-K MEDIUM HARVEST. (+{gained}% SOC)")

running_soc -= track['deploy_amount1']
print(f"- {track['deploy_corners']}: STANDARD DEPLOY. Short-burst acceleration. (-{track['deploy_amount1']}% SOC)")

print("\n[SECTOR 3]")
running_soc -= track['deploy_amount2']
print(f"- {track['s3_complex']}: STANDARD DEPLOY. Apex exit burst. (-{track['deploy_amount2']}% SOC)")

gained = process_harvest(track['final_harvest'])
running_soc += gained
print(f"- {track['final_corner']}: MGU-K HARVEST on entry. (+{gained}% SOC)")

if harvest_cap_triggered:
    print("- Main Straight: [FIA LIMIT REACHED] 7MJ energy cap triggered. MGU-K generation isolated.")
else:
    gained = process_harvest(4)
    running_soc += gained
    if harvest_cap_triggered:
        print("- Main Straight: [FIA LIMIT REACHED] 7MJ cap triggered mid-straight.")
    else:
        print(f"- Main Straight: Low-load harvest consolidation sequence active. (+{gained}% SOC)")

# --- 8. FINAL METRICS REPORTING ---
net_delta = running_soc - initial_soc

print("\n>> STINT METRICS <<")
print(f"Net Lap Delta: {net_delta}% Battery")
print(f"Terminal Lap SOC: {running_soc}%")

if running_soc < 20:
    print("\n[WARNING]: SOC below critical threshold (<20%). Toggle to RECHARGE engine mode.")
else:
    print("\n[STATUS]: ERS storage capacity parameters within acceptable operational bands.")
print("="*60)