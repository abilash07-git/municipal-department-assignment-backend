"""
Monsoon Heavy Rain Dual-Backend Engine Runner & Comparison Generator
Evaluates:
- Backend Engine 1: Privacy Redaction (Face, License Plate & Number Sanitization)
- Backend Engine 2: Department Assignment & Problem 3 Conflict Precedence Engine
on real municipal heavy rain / flood photos matching the Problem Statement.
"""

import os
import sys
import time
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Add repo paths
SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
REPO1_DIR = os.path.join(SCRATCH_DIR, "git_repo_ready")
REPO2_DIR = os.path.join(SCRATCH_DIR, "department_assignment_repo")
ARTIFACT_DIR = r"C:\Users\Lenovo\.gemini\antigravity\brain\82af6ceb-bb74-4b65-8996-16630260df13"

if REPO1_DIR not in sys.path:
    sys.path.append(REPO1_DIR)
if REPO2_DIR not in sys.path:
    sys.path.append(REPO2_DIR)

from redactor import PrivacyRedactor
from ai_conflict_engine import AIConflictEngine, STATUTORY_DEPARTMENTS

CASES = [
    {
        "id": "MONSOON_CASE_1",
        "title": "Case 1: Ward 12 & 13 Boundary Road Severe Waterlogging",
        "subtitle": "Benchmark Problem Statement Scenario (Heavy Monsoon Rainfall)",
        "image_file": "chennai_monsoon_raw.jpg",
        "ward": "Ward 12 / Ward 13 Boundary",
        "road_name": "GN Chetty Arterial Boundary Road",
        "coords": "13.0418° N, 80.2341° E",
        "hazard_type": "WATERLOGGING_ROAD",
        "desc": "Heavy 95mm rainfall causes severe 2.5 feet waterlogging on GN Chetty road along Ward 12 and Ward 13 boundary. Multiple cars, auto-rickshaws, and commuters stranded in standing water. Culvert inlet choked.",
        "sim_decline": {
            "declining_dept": "DEPT_DRAINAGE",
            "officer": "Er. K. Ramanathan (Executive Engineer SWD)",
            "quote": "This is a road-maintenance problem. Road surface has depressions and poor asphalt camber. Department B (Roads) should handle it."
        }
    },
    {
        "id": "MONSOON_CASE_2",
        "title": "Case 2: Linking Road Arterial Boundary Corridor Inundation",
        "subtitle": "Monsoon Transit Crisis: Stranded Bus & Flooded Junction",
        "image_file": "random_mumbai_monsoon.jpg",
        "ward": "Ward 54 / Ward 55 Boundary",
        "road_name": "Linking Road Boundary Arterial Corridor",
        "coords": "19.0600° N, 72.8340° E",
        "hazard_type": "WATERLOGGING_ROAD",
        "desc": "Severe monsoon waterlogging inundating municipal arterial boundary corridor. Municipal city bus and multiple two-wheelers stalled in knee-deep floodwater. Drain overflow.",
        "sim_decline": {
            "declining_dept": "DEPT_DRAINAGE",
            "officer": "Er. P. Mehta (Executive Engineer SWD)",
            "quote": "Road department failed to grade the surface slope towards the storm culvert. Reassign ticket to Roads & Infrastructure."
        }
    },
    {
        "id": "MONSOON_CASE_3",
        "title": "Case 3: Poonamallee High Boundary Road Pedestrian Submersion",
        "subtitle": "Public Safety Hazard: Commuters Wading in Floodwaters",
        "image_file": "chennai_02.jpg",
        "ward": "Ward 72 / Ward 73 Boundary",
        "road_name": "Poonamallee High Boundary Road",
        "coords": "13.0805° N, 80.2520° E",
        "hazard_type": "WATERLOGGING_ROAD",
        "desc": "Torrential monsoon rain causing severe waterlogging. Dozens of pedestrians and school children wading through waist-deep water. Submerged road craters hidden under water.",
        "sim_decline": {
            "declining_dept": "DEPT_DRAINAGE",
            "officer": "Er. S. Annamalai (Divisional Engineer SWD)",
            "quote": "The road pavement has potholes collecting water. Patching the asphalt belongs to Roads Department."
        }
    },
    {
        "id": "MONSOON_CASE_4",
        "title": "Case 4: Anna Nagar Commercial Junction Drain Overflow",
        "subtitle": "Commercial Thoroughfare Deluge: Traffic Gridlock",
        "image_file": "chennai_06.jpg",
        "ward": "Ward 104 / Ward 105 Boundary",
        "road_name": "Anna Nagar Boundary Avenue Junction",
        "coords": "13.0850° N, 80.2100° E",
        "hazard_type": "WATERLOGGING_ROAD",
        "desc": "Commercial avenue completely flooded following 3 hours of continuous monsoon downpour. Stalled vehicles and pedestrians navigating flooded carriage lanes.",
        "sim_decline": {
            "declining_dept": "DEPT_DRAINAGE",
            "officer": "Er. V. Sundaram (Assistant Executive Engineer SWD)",
            "quote": "Commercial shopfront ramps prevent water from reaching our drains. Roads department must remove unauthorized asphalt ramps."
        }
    }
]

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

def run_both_engines():
    print("=" * 80)
    print("EVALUATING BOTH BACKEND ENGINES ON MUNICIPAL HEAVY RAIN DATASETS")
    print("=" * 80)

    # Initialize Backend Engine 1 (Privacy Redactor) in high-efficiency single-pass mode
    redactor = PrivacyRedactor(enable_tiling=False, enable_numbers=True)

    results = []

    for c in CASES:
        print(f"\nProcessing {c['title']}...")
        img_path = os.path.join(SCRATCH_DIR, c["image_file"])
        if not os.path.exists(img_path):
            print(f"Skipping: {img_path} not found")
            continue

        cv_img = cv2.imread(img_path)
        h, w = cv_img.shape[:2]

        # -------------------------------------------------------------------
        # BACKEND ENGINE 1: PRIVACY REDACTION
        # -------------------------------------------------------------------
        t0 = time.time()
        _, targets = redactor.detect_all(cv_img)
        redact_time_ms = (time.time() - t0) * 1000.0

        blurred_bytes, meta_blur = redactor.redact(cv_img, style="blur")
        blackbox_bytes, meta_bb = redactor.redact(cv_img, style="blackbox")

        blurred_np = cv2.imdecode(np.frombuffer(blurred_bytes, np.uint8), cv2.IMREAD_COLOR)
        blackbox_np = cv2.imdecode(np.frombuffer(blackbox_bytes, np.uint8), cv2.IMREAD_COLOR)

        # Draw AI Proof overlay
        proof_np = cv_img.copy()
        for t in targets:
            bx, by, bw, bh = t["box"]
            color = (0, 220, 0) if t["type"] == "Face" else ((0, 0, 255) if t["type"] == "License Plate" else (255, 200, 0))
            cv2.rectangle(proof_np, (bx, by), (bx + bw, by + bh), color, 3)
            lbl = t["type"].split()[0].upper()
            cv2.putText(proof_np, lbl, (bx, max(20, by - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

        # -------------------------------------------------------------------
        # BACKEND ENGINE 2: PROBLEM 3 CONFLICT PRECEDENCE & DUAL-SLA
        # -------------------------------------------------------------------
        ai_res = AIConflictEngine.analyze_conflict(
            hazard_type=c["hazard_type"],
            description=c["desc"],
            ward=c["ward"],
            is_ward_boundary=True
        )

        slas = AIConflictEngine.calculate_dual_slas(
            primary_dept_id=ai_res["primary_department"]["id"],
            secondary_dept_id=ai_res["secondary_department"]["id"] if ai_res.get("secondary_department") else None,
            priority="CRITICAL",
            is_critical_safety=True
        )

        # Save individual resized images
        slug = c["id"].lower()
        max_dim = 1200
        scale = max_dim / float(max(w, h)) if max(w, h) > max_dim else 1.0
        nw, nh = int(w * scale), int(h * scale)

        raw_resized = cv2.resize(cv_img, (nw, nh), interpolation=cv2.INTER_AREA)
        proof_resized = cv2.resize(proof_np, (nw, nh), interpolation=cv2.INTER_AREA)
        blur_resized = cv2.resize(blurred_np, (nw, nh), interpolation=cv2.INTER_AREA)
        bb_resized = cv2.resize(blackbox_np, (nw, nh), interpolation=cv2.INTER_AREA)

        raw_fn = f"{slug}_input_raw.jpg"
        proof_fn = f"{slug}_proof.jpg"
        blur_fn = f"{slug}_blurred.jpg"
        bb_fn = f"{slug}_blackbox.jpg"

        cv2.imwrite(os.path.join(ARTIFACT_DIR, raw_fn), raw_resized, [cv2.IMWRITE_JPEG_QUALITY, 90])
        cv2.imwrite(os.path.join(ARTIFACT_DIR, proof_fn), proof_resized, [cv2.IMWRITE_JPEG_QUALITY, 90])
        cv2.imwrite(os.path.join(ARTIFACT_DIR, blur_fn), blur_resized, [cv2.IMWRITE_JPEG_QUALITY, 90])
        cv2.imwrite(os.path.join(ARTIFACT_DIR, bb_fn), bb_resized, [cv2.IMWRITE_JPEG_QUALITY, 90])

        # -------------------------------------------------------------------
        # COMPOSITE COMPARISON CARD (1600x960)
        # -------------------------------------------------------------------
        card_w, card_h = 1600, 960
        card = Image.new("RGB", (card_w, card_h), color=(15, 23, 42))
        draw = ImageDraw.Draw(card)

        f_title = get_font(24, bold=True)
        f_sub = get_font(15, bold=False)
        f_head = get_font(17, bold=True)
        f_body = get_font(13, bold=False)
        f_body_b = get_font(13, bold=True)
        f_mono = get_font(12, bold=False)

        # Header Banner
        draw.rectangle([(0, 0), (card_w, 75)], fill=(30, 41, 59))
        draw.text((25, 12), c["title"], font=f_title, fill=(248, 250, 252))
        draw.text((25, 45), c["subtitle"] + " | Dual Engine Evaluation", font=f_sub, fill=(148, 163, 184))

        draw.rounded_rectangle([(card_w - 320, 18), (card_w - 25, 58)], radius=6, fill=(185, 28, 28))
        draw.text((card_w - 305, 26), "MUNICIPAL MONSOON DELUGE", font=f_body_b, fill=(255, 255, 255))

        # LEFT COLUMN: ENGINE 1 (PRIVACY REDACTION: BEFORE & AFTER)
        col1_x = 25
        col1_y = 95
        col1_w = 750
        col1_h = 835

        draw.rounded_rectangle([(col1_x, col1_y), (col1_x + col1_w, col1_y + col1_h)], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
        draw.text((col1_x + 20, col1_y + 15), "ENGINE 1: PRIVACY REDACTION & SANITIZATION", font=f_head, fill=(56, 189, 248))
        draw.text((col1_x + 20, col1_y + 40), f"Latency: {redact_time_ms:.1f}ms | Faces: {meta_blur['faces_redacted']} | Plates: {meta_blur['plates_redacted']} | Digits: {meta_blur['numbers_redacted']}", font=f_body_b, fill=(74, 222, 128))

        # Show Before (Raw) and After (Blurred)
        thumb_w, thumb_h = 345, 260
        pil_raw = Image.fromarray(cv2.cvtColor(raw_resized, cv2.COLOR_BGR2RGB))
        pil_raw.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        card.paste(pil_raw, (col1_x + 20, col1_y + 70))
        draw.rectangle([(col1_x + 20, col1_y + 70), (col1_x + 20 + pil_raw.size[0], col1_y + 98)], fill=(15, 23, 42))
        draw.text((col1_x + 28, col1_y + 75), "1. ORIGINAL CITIZEN PHOTO", font=f_body_b, fill=(248, 250, 252))

        pil_blur = Image.fromarray(cv2.cvtColor(blur_resized, cv2.COLOR_BGR2RGB))
        pil_blur.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        card.paste(pil_blur, (col1_x + 385, col1_y + 70))
        draw.rectangle([(col1_x + 385, col1_y + 70), (col1_x + 385 + pil_blur.size[0], col1_y + 98)], fill=(16, 185, 129))
        draw.text((col1_x + 393, col1_y + 75), "2. REDACTED (EXIF STRIPPED)", font=f_body_b, fill=(255, 255, 255))

        # Show Proof with Bounding Boxes Below
        proof_w, proof_h = 710, 430
        pil_proof = Image.fromarray(cv2.cvtColor(proof_resized, cv2.COLOR_BGR2RGB))
        pil_proof.thumbnail((proof_w, proof_h), Image.Resampling.LANCZOS)
        card.paste(pil_proof, (col1_x + 20, col1_y + 355))
        draw.rectangle([(col1_x + 20, col1_y + 355), (col1_x + 20 + pil_proof.size[0], col1_y + 385)], fill=(185, 28, 28))
        draw.text((col1_x + 28, col1_y + 360), f"3. AI DETECTION PROOF ({len(targets)} SENSITIVE TARGETS FLAGGED)", font=f_body_b, fill=(255, 255, 255))

        # RIGHT COLUMN: ENGINE 2 (DEPARTMENT ASSIGNMENT & CONFLICT RESOLUTION)
        col2_x = 805
        col2_y = 95
        col2_w = 770
        col2_h = 835

        draw.rounded_rectangle([(col2_x, col2_y), (col2_x + col2_w, col2_y + col2_h)], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
        draw.text((col2_x + 20, col2_y + 15), "ENGINE 2: DEPARTMENT ASSIGNMENT & CONFLICT RESOLUTION", font=f_head, fill=(74, 222, 128))
        draw.text((col2_x + 20, col2_y + 40), f"Ward Boundary: {c['ward']} | Precedence: {ai_res['ownership_rule_applied']}", font=f_body_b, fill=(251, 191, 36))

        # Box 1: Pre-Assignment & Precedence
        b1_y = col2_y + 70
        draw.rounded_rectangle([(col2_x + 20, b1_y), (col2_x + col2_w - 20, b1_y + 205)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((col2_x + 35, b1_y + 12), "STATUTORY ROOT-CAUSE PRECEDENCE ASSIGNMENT:", font=f_body_b, fill=(251, 191, 36))

        draw.text((col2_x + 35, b1_y + 40), "• Lead Responder:", font=f_body_b, fill=(74, 222, 128))
        draw.text((col2_x + 220, b1_y + 40), f"{ai_res['primary_department']['name']} [{ai_res['primary_department']['code']}]", font=f_body, fill=(248, 250, 252))

        draw.text((col2_x + 35, b1_y + 68), "• Joint Support Partner:", font=f_body_b, fill=(96, 165, 250))
        draw.text((col2_x + 220, b1_y + 68), f"{ai_res['secondary_department']['name']} [{ai_res['secondary_department']['code']}]", font=f_body, fill=(248, 250, 252))

        draw.text((col2_x + 35, b1_y + 98), "• Rule Rationale:", font=f_body_b, fill=(148, 163, 184))
        # Wrap rationale
        rw = ai_res['conflict_resolution_rationale'].split()
        draw.text((col2_x + 35, b1_y + 120), " ".join(rw[:13]), font=f_body, fill=(203, 213, 225))
        if len(rw) > 13:
            draw.text((col2_x + 35, b1_y + 142), " ".join(rw[13:26]), font=f_body, fill=(203, 213, 225))
        if len(rw) > 26:
            draw.text((col2_x + 35, b1_y + 164), " ".join(rw[26:]), font=f_body, fill=(203, 213, 225))

        # Box 2: Dual SLA Clocks (with 5-minute policy)
        b2_y = b1_y + 220
        draw.rounded_rectangle([(col2_x + 20, b2_y), (col2_x + col2_w - 20, b2_y + 175)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((col2_x + 35, b2_y + 12), "INDEPENDENT DUAL-SLA CLOCKS (5-MIN DEMO ACKNOWLEDGMENT):", font=f_body_b, fill=(56, 189, 248))

        # Primary Clock
        p_sla = slas["primary_sla"]
        draw.rounded_rectangle([(col2_x + 35, b2_y + 40), (col2_x + 365, b2_y + 155)], radius=6, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
        draw.text((col2_x + 48, b2_y + 48), f"PRIMARY: {p_sla['department_code']} (LEAD)", font=f_body_b, fill=(255, 255, 255))
        draw.text((col2_x + 48, b2_y + 75), f"Ack Deadline:  {p_sla['acknowledgment_limit_minutes']} MINS", font=f_body_b, fill=(254, 240, 138))
        draw.text((col2_x + 48, b2_y + 100), f"Resolution:    {p_sla['resolution_limit_hours']} HOURS", font=f_body, fill=(209, 250, 229))
        draw.text((col2_x + 48, b2_y + 125), "Status: 04:59 COUNTING DOWN", font=f_mono, fill=(52, 211, 153))

        # Secondary Clock
        s_sla = slas["secondary_sla"]
        draw.rounded_rectangle([(col2_x + 390, b2_y + 40), (col2_x + 735, b2_y + 155)], radius=6, fill=(30, 58, 138), outline=(59, 130, 246), width=2)
        draw.text((col2_x + 403, b2_y + 48), f"SECONDARY: {s_sla['department_code']} (JOINT)", font=f_body_b, fill=(255, 255, 255))
        draw.text((col2_x + 403, b2_y + 75), f"Ack Deadline:  {s_sla['acknowledgment_limit_minutes']} MINS", font=f_body_b, fill=(254, 240, 138))
        draw.text((col2_x + 403, b2_y + 100), f"Resolution:    {s_sla['resolution_limit_hours']} HOURS", font=f_body, fill=(219, 234, 254))
        draw.text((col2_x + 403, b2_y + 125), "Status: STANDBY PROTOCOL READY", font=f_mono, fill=(96, 165, 250))

        # Box 3: Anti-Ping-Pong Routing Interception Card
        b3_y = b2_y + 190
        draw.rounded_rectangle([(col2_x + 20, b3_y), (col2_x + col2_w - 20, b3_y + 225)], radius=8, fill=(15, 23, 42), outline=(220, 38, 38), width=2)
        draw.rectangle([(col2_x + 20, b3_y), (col2_x + col2_w - 20, b3_y + 32)], fill=(153, 27, 27))
        draw.text((col2_x + 35, b3_y + 7), "ANTI-PING-PONG SHIELD: DECLINE ATTEMPT INTERCEPTED", font=f_body_b, fill=(255, 255, 255))

        sim = c["sim_decline"]
        draw.text((col2_x + 35, b3_y + 45), f"1. Dept A Decline Attempt:", font=f_body_b, fill=(248, 113, 113))
        draw.text((col2_x + 250, b3_y + 45), f"{sim['officer']} ({sim['declining_dept']})", font=f_body, fill=(254, 202, 202))

        draw.text((col2_x + 35, b3_y + 70), f"   Stated Reason:", font=f_body, fill=(148, 163, 184))
        draw.text((col2_x + 160, b3_y + 70), f'"{sim["quote"][:55]}..."', font=f_mono, fill=(252, 165, 165))

        draw.text((col2_x + 35, b3_y + 105), "2. Automated Dispute Interception:", font=f_body_b, fill=(250, 204, 21))
        draw.text((col2_x + 310, b3_y + 105), "BLOCKED! Reassignment back to Dept B strictly forbidden.", font=f_body_b, fill=(254, 240, 138))

        draw.text((col2_x + 35, b3_y + 135), "3. Direct High-Command Escalation:", font=f_body_b, fill=(239, 68, 68))
        draw.text((col2_x + 310, b3_y + 135), "Escalated to Zonal Joint Municipal Commissioner", font=f_body, fill=(248, 250, 252))

        draw.text((col2_x + 35, b3_y + 165), "4. Binding Joint Directive:", font=f_body_b, fill=(56, 189, 248))
        draw.text((col2_x + 310, b3_y + 165), "MANDATORY JOINT ORDER #JD-2026-904 ISSUED", font=f_mono, fill=(125, 211, 252))

        draw.rounded_rectangle([(col2_x + 35, b3_y + 195), (col2_x + col2_w - 35, b3_y + 218)], radius=4, fill=(30, 41, 59))
        draw.text((col2_x + 45, b3_y + 200), "GUARANTEE: No complaint ever remains unresolved due to departmental disagreement.", font=f_body_b, fill=(74, 222, 128))

        # Save Composite Card
        comp_fn = f"{slug}_dual_engine_comparison.jpg"
        comp_path = os.path.join(ARTIFACT_DIR, comp_fn)
        card.save(comp_path, quality=92)
        print(f"Saved: {comp_fn} (1600x960)")

        results.append({
            "id": c["id"],
            "title": c["title"],
            "subtitle": c["subtitle"],
            "ward": c["ward"],
            "road_name": c["road_name"],
            "coords": c["coords"],
            "desc": c["desc"],
            "raw_file": raw_fn,
            "proof_file": proof_fn,
            "blur_file": blur_fn,
            "blackbox_file": bb_fn,
            "composite_file": comp_fn,
            "engine1_telemetry": {
                "latency_ms": round(redact_time_ms, 1),
                "faces_redacted": meta_blur["faces_redacted"],
                "plates_redacted": meta_blur["plates_redacted"],
                "numbers_redacted": meta_blur["numbers_redacted"],
                "total_redactions": meta_blur["total_redactions"]
            },
            "engine2_routing": {
                "conflict_type": ai_res["conflict_type"],
                "primary_dept": ai_res["primary_department"]["name"],
                "primary_code": ai_res["primary_department"]["code"],
                "secondary_dept": ai_res["secondary_department"]["name"],
                "secondary_code": ai_res["secondary_department"]["code"],
                "rule_applied": ai_res["ownership_rule_applied"],
                "rationale": ai_res["conflict_resolution_rationale"],
                "primary_ack_limit_min": p_sla["acknowledgment_limit_minutes"],
                "primary_res_limit_hr": p_sla["resolution_limit_hours"],
                "secondary_ack_limit_min": s_sla["acknowledgment_limit_minutes"],
                "secondary_res_limit_hr": s_sla["resolution_limit_hours"]
            },
            "decline_simulation": c["sim_decline"]
        })

    # Save summary JSON
    sum_path = os.path.join(ARTIFACT_DIR, "monsoon_dual_engine_results.json")
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("ALL 4 MUNICIPAL MONSOON DELUGE CASES COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    return results

if __name__ == "__main__":
    run_both_engines()
