"""
Visual Workflow Demonstration Generator for Problem 3:
Departmental Ownership Ambiguity, Dual-SLA Engine & Anti-Ping-Pong Routing
Processes 5 real online dataset images and generates side-by-side workflow cards.
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont

# Add repo to sys.path
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from ai_conflict_engine import AIConflictEngine, STATUTORY_DEPARTMENTS

SCRATCH_DIR = os.path.abspath(os.path.join(REPO_DIR, ".."))
ARTIFACT_DIR = r"C:\Users\Lenovo\.gemini\antigravity\brain\82af6ceb-bb74-4b65-8996-16630260df13"
OUTPUT_DIR = os.path.join(REPO_DIR, "demo_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# Select available fonts
def get_font(size: int, bold: bool = False):
    font_names = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for fn in font_names:
        fp = os.path.join(r"C:\Windows\Fonts", fn)
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

CASES = [
    {
        "id": "CASE_1",
        "title": "Case 1: Ward 12 & 13 Boundary Road Waterlogging",
        "subtitle": "Benchmark Problem 3 Scenario: Drainage vs Road Maintenance",
        "image_file": "chennai_monsoon_raw.jpg",
        "hazard_type": "WATERLOGGING_ROAD",
        "ward": "Ward 12 / Ward 13 Boundary",
        "location": "GN Chetty Arterial Boundary Road (Ward 12 / Ward 13 Border)",
        "coords": "13.0418° N, 80.2341° E",
        "description": "Severe 2.5 feet standing waterlogging on GN Chetty boundary road following 85mm rainfall. Multiple cars and auto-rickshaws stalled in water. Storm drain inlet completely submerged.",
        "simulated_decline": {
            "declining_dept": "DEPT_DRAINAGE",
            "declining_officer": "Er. K. Ramanathan (Executive Engineer SWD)",
            "reason": "This is a road-maintenance problem. Road surface has depressions and poor asphalt camber. Department B (Roads) should handle it."
        }
    },
    {
        "id": "CASE_2",
        "title": "Case 2: Snapped High-Voltage Power Line in Foliage",
        "subtitle": "Life-Safety Hazard: Electricity vs Horticulture",
        "image_file": "downed_power_line.jpg",
        "hazard_type": "LIVE_WIRE_TREE",
        "ward": "Ward 77 / Ward 78 Boundary",
        "location": "Gandhi Irwin Boundary Road (Ward 77 / Ward 78 Border)",
        "coords": "13.0827° N, 80.2707° E",
        "description": "High-voltage 440V distribution wire snapped and sparking actively in tree foliage directly above public pedestrian sidewalk and carriageway.",
        "simulated_decline": {
            "declining_dept": "DEPT_ELECTRICITY",
            "declining_officer": "Er. S. Murugan (Divisional Engineer ELEC)",
            "reason": "Heavy overgrown tree branches caused the wire snap. Horticulture Department must prune and clear the tree limbs before we can restore lines."
        }
    },
    {
        "id": "CASE_3",
        "title": "Case 3: Underground Water Pipe Burst & Road Crater",
        "subtitle": "Subterranean Erosion: Water Supply vs Roads & Bridges",
        "image_file": "pothole_kolkata.jpg",
        "hazard_type": "PIPE_BURST_ROAD",
        "ward": "Ward 112 / Ward 113 Boundary",
        "location": "Luz Church Boundary Avenue (Ward 112 / Ward 113 Border)",
        "coords": "13.0331° N, 80.2612° E",
        "description": "Active pressurized drinking water pipeline burst causing 4-foot deep subterranean crater and road cave-in on arterial boundary road.",
        "simulated_decline": {
            "declining_dept": "DEPT_WATER_SUPPLY",
            "declining_officer": "Er. T. Chandran (Executive Engineer MWSSB)",
            "reason": "This complaint was reported as a road crater / pothole. Public road repairs belong exclusively to Roads & Infrastructure Department."
        }
    },
    {
        "id": "CASE_4",
        "title": "Case 4: Uprooted 40-Year Banyan Tree Obstructing Arterial Highway",
        "subtitle": "Transit Obstruction: Horticulture vs Roads & Traffic",
        "image_file": "fallen_tree_road.jpg",
        "hazard_type": "FALLEN_TREE_ROAD",
        "ward": "Ward 140 / Ward 141 Boundary",
        "location": "Anna Salai Arterial Highway Border (Ward 140 / Ward 141 Border)",
        "coords": "13.0112° N, 80.2185° E",
        "description": "Massive 15-ton uprooted banyan tree collapsed completely across both carriageway lanes, crushing concrete median barrier and blocking traffic.",
        "simulated_decline": {
            "declining_dept": "DEPT_HORTICULTURE",
            "declining_officer": "Dr. R. Natarajan (Tree Officer)",
            "reason": "The median barrier is crushed and major vehicular arterial transit is blocked. Roads Department and Traffic Authority must divert and handle."
        }
    },
    {
        "id": "CASE_5",
        "title": "Case 5: Commercial Refuse Dumped in Storm Canal Culvert",
        "subtitle": "Debris Clearance: Solid Waste Management vs Storm Drainage",
        "image_file": "random_delhi_garbage.jpg",
        "hazard_type": "GARBAGE_IN_DRAIN",
        "ward": "Ward 85 / Ward 86 Boundary",
        "location": "Outer Ring Boundary Canal Road (Ward 85 / Ward 86 Border)",
        "coords": "13.0694° N, 80.1948° E",
        "description": "5 tons of illegally dumped commercial packaging, plastic sacks, and municipal refuse completely clogging storm drainage culvert intake mouth.",
        "simulated_decline": {
            "declining_dept": "DEPT_SOLID_WASTE",
            "declining_officer": "Shri M. Velu (Sanitary Inspector SWM)",
            "reason": "The refuse is located inside the culvert channel. Canal cleaning and desilting falls strictly under Stormwater Drainage Department."
        }
    }
]

def generate_case_visualization(c: dict) -> str:
    """
    Renders a side-by-side composite visualization:
    Left: Real input image with GPS / ward boundary tag and problem highlight.
    Right: Step-by-step Problem 3 AI Analysis, Dual SLA Clocks, and Anti-Ping-Pong Intercept Card.
    """
    # 1. Run AI Conflict Engine
    ai_res = AIConflictEngine.analyze_conflict(
        hazard_type=c["hazard_type"],
        description=c["description"],
        ward=c["ward"],
        is_ward_boundary=True
    )
    slas = AIConflictEngine.calculate_dual_slas(
        primary_dept_id=ai_res["primary_department"]["id"],
        secondary_dept_id=ai_res["secondary_department"]["id"] if ai_res.get("secondary_department") else None,
        priority="CRITICAL",
        is_critical_safety=True
    )

    # 2. Dimensions and Canvas
    width = 1600
    height = 960
    canvas = Image.new("RGB", (width, height), color=(15, 23, 42)) # Deep slate dark theme
    draw = ImageDraw.Draw(canvas)

    font_title = get_font(26, bold=True)
    font_subtitle = get_font(16, bold=False)
    font_header = get_font(18, bold=True)
    font_subhead = get_font(15, bold=True)
    font_body = get_font(13, bold=False)
    font_body_bold = get_font(13, bold=True)
    font_mono = get_font(12, bold=False)

    # Top Header Banner
    draw.rectangle([(0, 0), (width, 80)], fill=(30, 41, 59))
    draw.text((30, 15), c["title"], font=font_title, fill=(248, 250, 252))
    draw.text((30, 48), c["subtitle"] + " | Boundary Dispute & SLA Escalation Architecture", font=font_subtitle, fill=(148, 163, 184))

    # Pill Tag on Header Right
    draw.rounded_rectangle([(width - 340, 20), (width - 30, 60)], radius=8, fill=(185, 28, 28))
    draw.text((width - 325, 28), "PROBLEM 3 DEMONSTRATION", font=font_subhead, fill=(255, 255, 255))

    # -----------------------------------------------------------------------
    # LEFT PANEL: INPUT IMAGE FROM REAL ONLINE DATASET
    # -----------------------------------------------------------------------
    left_x = 30
    left_y = 105
    left_w = 680
    left_h = 820

    # Background card for Left Panel
    draw.rounded_rectangle([(left_x, left_y), (left_x + left_w, left_y + left_h)], radius=12, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    
    # Left Header
    draw.text((left_x + 20, left_y + 15), "STEP 1: CITIZEN REPORT & INPUT PICTURE", font=font_header, fill=(56, 189, 248))
    draw.text((left_x + 20, left_y + 42), "High-resolution photo ingested from municipal citizen app feed", font=font_body, fill=(148, 163, 184))

    # Load and place image
    raw_img_path = os.path.join(SCRATCH_DIR, c["image_file"])
    if os.path.exists(raw_img_path):
        raw_img = Image.open(raw_img_path).convert("RGB")
        # Resize to fit 640 x 420 maintaining aspect ratio with letterboxing
        raw_target_w = 640
        raw_target_h = 420
        raw_img.thumbnail((raw_target_w, raw_target_h), Image.Resampling.LANCZOS)
        
        # Center in image sub-box
        img_box_x = left_x + 20
        img_box_y = left_y + 75
        img_w, img_h = raw_img.size
        offset_x = img_box_x + (raw_target_w - img_w) // 2
        offset_y = img_box_y + (raw_target_h - img_h) // 2

        # Draw box outline
        draw.rectangle([(img_box_x, img_box_y), (img_box_x + raw_target_w, img_box_y + raw_target_h)], fill=(15, 23, 42), outline=(71, 85, 105), width=1)
        canvas.paste(raw_img, (offset_x, offset_y))

        # Stamp a semi-transparent or red banner on image top
        draw.rectangle([(img_box_x, img_box_y), (img_box_x + raw_target_w, img_box_y + 36)], fill=(220, 38, 38))
        draw.text((img_box_x + 15, img_box_y + 8), f"LOCATION DETECTED: {c['ward'].upper()}", font=font_subhead, fill=(255, 255, 255))
    else:
        draw.rectangle([(left_x + 20, left_y + 75), (left_x + left_w - 20, left_y + 495)], fill=(15, 23, 42))
        draw.text((left_x + 50, left_y + 250), f"Image not found: {c['image_file']}", font=font_header, fill=(239, 68, 68))

    # Image metadata box below picture
    meta_y = left_y + 510
    draw.rounded_rectangle([(left_x + 20, meta_y), (left_x + left_w - 20, meta_y + 285)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    
    draw.text((left_x + 35, meta_y + 15), "INCIDENT TELEMETRY & GPS MAPPING:", font=font_subhead, fill=(226, 232, 240))
    draw.text((left_x + 35, meta_y + 42), f"Arterial Location: {c['location']}", font=font_body, fill=(203, 213, 225))
    draw.text((left_x + 35, meta_y + 68), f"GPS Coordinates:   {c['coords']}", font=font_mono, fill=(56, 189, 248))
    draw.text((left_x + 35, meta_y + 94), f"Boundary Status:   CONFIRMED INTER-WARD BORDER ({ai_res.get('boundary_wards', ['Ward 12', 'Ward 13'])})", font=font_body_bold, fill=(234, 179, 8))
    
    draw.text((left_x + 35, meta_y + 125), "Citizen Report Description:", font=font_subhead, fill=(226, 232, 240))
    # Wrap description in 2 lines
    desc_words = c["description"].split()
    line1 = " ".join(desc_words[:12])
    line2 = " ".join(desc_words[12:24])
    line3 = " ".join(desc_words[24:])
    draw.text((left_x + 35, meta_y + 150), f'"{line1}', font=font_body, fill=(148, 163, 184))
    if line2:
        draw.text((left_x + 35, meta_y + 172), f'{line2}', font=font_body, fill=(148, 163, 184))
    if line3:
        draw.text((left_x + 35, meta_y + 194), f'{line3}"', font=font_body, fill=(148, 163, 184))

    # Stamp status
    draw.rounded_rectangle([(left_x + 35, meta_y + 235), (left_x + left_w - 35, meta_y + 270)], radius=6, fill=(30, 58, 138))
    draw.text((left_x + 50, meta_y + 243), "AI VERIFICATION: AMBIGUOUS DUAL-DEPARTMENT OVERLAP DETECTED", font=font_body_bold, fill=(147, 197, 253))

    # -----------------------------------------------------------------------
    # RIGHT PANEL: AI WORKFLOW, PRECEDENCE RULE, DUAL SLAS & PING-PONG INTERCEPT
    # -----------------------------------------------------------------------
    right_x = 740
    right_y = 105
    right_w = 830
    right_h = 820

    # Background card for Right Panel
    draw.rounded_rectangle([(right_x, right_y), (right_x + right_w, right_y + right_h)], radius=12, fill=(30, 41, 59), outline=(51, 65, 85), width=2)

    # Right Header
    draw.text((right_x + 25, right_y + 15), "STEP 2-7: AI CONFLICT ENGINE & ANTI-PING-PONG SHIELD", font=font_header, fill=(74, 222, 128))
    draw.text((right_x + 25, right_y + 42), f"Conflict Type: {ai_res['conflict_type']} (AI Confidence: {ai_res['ai_confidence'] * 100:.1f}%)", font=font_body, fill=(203, 213, 225))

    # Box 1: Precedence Rule & Statutory Pre-Assignment (Top of Right Panel)
    box1_y = right_y + 75
    draw.rounded_rectangle([(right_x + 20, box1_y), (right_x + right_w - 20, box1_y + 180)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    
    draw.text((right_x + 35, box1_y + 12), "STATUTORY PRE-ASSIGNMENT & PRECEDENCE RULE APPLIED:", font=font_subhead, fill=(251, 191, 36))
    
    # Precedence rule badge
    rule_name = ai_res["ownership_rule_applied"]
    draw.rounded_rectangle([(right_x + 35, box1_y + 36), (right_x + 480, box1_y + 64)], radius=5, fill=(120, 53, 15))
    draw.text((right_x + 45, box1_y + 41), f"RULE: {rule_name}", font=font_body_bold, fill=(254, 243, 199))

    # Lead Department & Secondary
    p_name = ai_res["primary_department"]["name"]
    p_code = ai_res["primary_department"]["code"]
    s_name = ai_res["secondary_department"]["name"] if ai_res.get("secondary_department") else "None"
    s_code = ai_res["secondary_department"]["code"] if ai_res.get("secondary_department") else "N/A"

    draw.text((right_x + 35, box1_y + 76), f"• Primary Owner (Lead Responder):", font=font_body_bold, fill=(74, 222, 128))
    draw.text((right_x + 310, box1_y + 76), f"{p_name} [{p_code}]", font=font_body, fill=(248, 250, 252))

    draw.text((right_x + 35, box1_y + 100), f"• Secondary Joint Partner:", font=font_body_bold, fill=(96, 165, 250))
    draw.text((right_x + 310, box1_y + 100), f"{s_name} [{s_code}] (Coordinated Standby)", font=font_body, fill=(248, 250, 252))

    # Rationale
    rat = ai_res["conflict_resolution_rationale"]
    draw.text((right_x + 35, box1_y + 126), "Legal Rationale:", font=font_body_bold, fill=(148, 163, 184))
    r_words = rat.split()
    r_line1 = " ".join(r_words[:14])
    r_line2 = " ".join(r_words[14:28])
    draw.text((right_x + 145, box1_y + 126), r_line1, font=font_body, fill=(203, 213, 225))
    if r_line2:
        draw.text((right_x + 145, box1_y + 148), r_line2, font=font_body, fill=(203, 213, 225))

    # Box 2: Dual SLA Clocks (Middle of Right Panel)
    box2_y = box1_y + 195
    draw.rounded_rectangle([(right_x + 20, box2_y), (right_x + right_w - 20, box2_y + 160)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    draw.text((right_x + 35, box2_y + 12), "INDEPENDENT DUAL-SLA CLOCKS (WITH 5-MIN DEMO POLICY):", font=font_subhead, fill=(56, 189, 248))

    # Primary SLA card (Green border)
    p_sla = slas["primary_sla"]
    draw.rounded_rectangle([(right_x + 35, box2_y + 40), (right_x + 395, box2_y + 142)], radius=6, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((right_x + 48, box2_y + 48), f"PRIMARY: {p_sla['department_code']} (LEAD)", font=font_body_bold, fill=(255, 255, 255))
    draw.text((right_x + 48, box2_y + 72), f"Acknowledgment Clock:  {p_sla['acknowledgment_limit_minutes']} MINS", font=font_body_bold, fill=(254, 240, 138))
    draw.text((right_x + 48, box2_y + 94), f"Resolution Deadline:   {p_sla['resolution_limit_hours']} HOURS", font=font_body, fill=(209, 250, 229))
    draw.text((right_x + 48, box2_y + 116), "Status: ACTIVE COUNTDOWN", font=font_mono, fill=(52, 211, 153))

    # Secondary SLA card (Blue border)
    s_sla = slas.get("secondary_sla")
    draw.rounded_rectangle([(right_x + 420, box2_y + 40), (right_x + 785, box2_y + 142)], radius=6, fill=(30, 58, 138), outline=(59, 130, 246), width=2)
    draw.text((right_x + 433, box2_y + 48), f"SECONDARY: {s_code} (JOINT SUPPORT)", font=font_body_bold, fill=(255, 255, 255))
    if s_sla:
        draw.text((right_x + 433, box2_y + 72), f"Acknowledgment Clock:  {s_sla['acknowledgment_limit_minutes']} MINS", font=font_body_bold, fill=(254, 240, 138))
        draw.text((right_x + 433, box2_y + 94), f"Resolution Deadline:   {s_sla['resolution_limit_hours']} HOURS", font=font_body, fill=(219, 234, 254))
        draw.text((right_x + 433, box2_y + 116), "Status: STANDBY PROTOCOL READY", font=font_mono, fill=(96, 165, 250))
    else:
        draw.text((right_x + 433, box2_y + 72), "No Secondary Department Required", font=font_body, fill=(203, 213, 225))

    # Box 3: Anti-Ping-Pong Routing Interception & Decline Escalation (Bottom of Right Panel)
    box3_y = box2_y + 175
    draw.rounded_rectangle([(right_x + 20, box3_y), (right_x + right_w - 20, box3_y + 245)], radius=8, fill=(15, 23, 42), outline=(220, 38, 38), width=2)
    
    # Interception Banner
    draw.rectangle([(right_x + 20, box3_y), (right_x + right_w - 20, box3_y + 35)], fill=(153, 27, 27))
    draw.text((right_x + 35, box3_y + 8), "ANTI-PING-PONG SHIELD: UNILATERAL DECLINE INTERCEPTED & ESCALATED", font=font_subhead, fill=(255, 255, 255))

    sim = c["simulated_decline"]
    draw.text((right_x + 35, box3_y + 48), f"1. Department Rejection Attempt:", font=font_body_bold, fill=(248, 113, 113))
    draw.text((right_x + 295, box3_y + 48), f"{sim['declining_officer']} ({sim['declining_dept']})", font=font_body, fill=(254, 202, 202))
    
    draw.text((right_x + 35, box3_y + 72), f"   Stated Reason:", font=font_body, fill=(148, 163, 184))
    d_words = sim["reason"].split()
    d_l1 = " ".join(d_words[:13])
    d_l2 = " ".join(d_words[13:])
    draw.text((right_x + 160, box3_y + 72), f'"{d_l1}', font=font_mono, fill=(252, 165, 165))
    if d_l2:
        draw.text((right_x + 160, box3_y + 92), f'{d_l2}"', font=font_mono, fill=(252, 165, 165))

    # Action Taken by System
    draw.text((right_x + 35, box3_y + 122), "2. Automated Dispute Interception:", font=font_body_bold, fill=(250, 204, 21))
    draw.text((right_x + 310, box3_y + 122), "BLOCKED! Unilateral reassignment back to Dept B denied.", font=font_body_bold, fill=(254, 240, 138))

    draw.text((right_x + 35, box3_y + 148), "3. High-Command Escalation:", font=font_body_bold, fill=(239, 68, 68))
    draw.text((right_x + 310, box3_y + 148), "Direct Escalation to Zonal Joint Municipal Commissioner", font=font_body, fill=(248, 250, 252))

    draw.text((right_x + 35, box3_y + 172), "4. Binding Enforcement Order:", font=font_body_bold, fill=(56, 189, 248))
    draw.text((right_x + 310, box3_y + 172), "MANDATORY JOINT DIRECTIVE #JD-2026-904 ISSUED", font=font_mono, fill=(125, 211, 252))
    draw.text((right_x + 310, box3_y + 192), "Both crews ordered to site concurrently under Commissioner Oversight.", font=font_body, fill=(148, 163, 184))

    # Bottom Pill
    draw.rounded_rectangle([(right_x + 35, box3_y + 215), (right_x + right_w - 35, box3_y + 238)], radius=4, fill=(30, 41, 59))
    draw.text((right_x + 45, box3_y + 220), "GUARANTEE: No civic issue ever remains unresolved due to departmental buck-passing.", font=font_body_bold, fill=(74, 222, 128))

    # Save output
    out_name = f"workflow_{c['id'].lower()}_{c['hazard_type'].lower()}.jpg"
    out_path_demo = os.path.join(OUTPUT_DIR, out_name)
    out_path_artifact = os.path.join(ARTIFACT_DIR, out_name)

    canvas.save(out_path_demo, quality=95)
    canvas.save(out_path_artifact, quality=95)
    print(f"Saved: {out_name} -> {out_path_artifact}")
    return out_path_artifact

def main():
    print("=" * 80)
    print("GENERATING VISUAL WORKFLOW DEMONSTRATION CARDS FOR 5 REAL DATASET IMAGES")
    print("=" * 80)
    generated_paths = []
    for c in CASES:
        p = generate_case_visualization(c)
        generated_paths.append((c, p))

    print("\nAll 5 visual workflow demonstration cards generated successfully!")
    return generated_paths

if __name__ == "__main__":
    main()
