"""
Statutory Municipal Department Routing & Classification Engine
Provides automated problem classification, pre-routing to concerned departments,
dynamic urgency scoring, probabilistic SLA calculations, and anti-loop deadlock detection.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# STATUTORY MUNICIPAL DEPARTMENTS REGISTRY (INDIA)
# ---------------------------------------------------------------------------
STATUTORY_MUNICIPAL_DEPARTMENTS = {
    "DEPT_ELECTRICITY": {
        "id": "DEPT_ELECTRICITY",
        "name": "Electricity & Street Lighting Department",
        "code": "ELEC",
        "in_charge": "Superintending Engineer (Power Distribution & Street Lighting)",
        "handles": "Live snapped wires, sparking transformers, fallen electric poles, electric shock hazards in water, dark streetlights, open junction boxes",
        "alert_channel": "electricity-emergency@municipal.gov.in | VHF Ch-3 | Emergency Helpline 1912",
        "sla_hours": {"CRITICAL": 1, "HIGH": 3, "MEDIUM": 6, "LOW": 24},
        "keywords": ["wire", "electric", "current", "pole", "transformer", "spark", "cable", "shock", "streetlight", "power", "blackout", "lamp", "voltage"]
    },
    "DEPT_DRAINAGE": {
        "id": "DEPT_DRAINAGE",
        "name": "Stormwater Drainage & Flood Mitigation Department",
        "code": "SWD",
        "in_charge": "Executive Engineer (Stormwater Drainage & Flood Control)",
        "handles": "Water clogging, flooded roads, blocked culverts, open storm drain manholes, dewatering pump operations",
        "alert_channel": "drainage-emergency@municipal.gov.in | VHF Ch-4 | Flood Cell Hotline 1077",
        "sla_hours": {"CRITICAL": 2, "HIGH": 4, "MEDIUM": 8, "LOW": 24},
        "keywords": ["water", "clogging", "waterlogging", "flood", "drain", "gutter", "manhole", "culvert", "overflow", "stagnant", "submerged", "puddle"]
    },
    "DEPT_ROADS": {
        "id": "DEPT_ROADS",
        "name": "Roads & Infrastructure Department",
        "code": "ROADS",
        "in_charge": "Executive Engineer (Road Maintenance & Pothole Repair)",
        "handles": "Road potholes, asphalt craters, road cave-ins, broken paver blocks, damaged footpaths, flyover expansion joints",
        "alert_channel": "roads-repair@municipal.gov.in | VHF Ch-2 | Public Works Helpline 1916",
        "sla_hours": {"CRITICAL": 3, "HIGH": 6, "MEDIUM": 12, "LOW": 48},
        "keywords": ["pothole", "crater", "road", "asphalt", "cave-in", "pavement", "footpath", "tar", "divider", "damaged road", "surface", "rut"]
    },
    "DEPT_HORTICULTURE": {
        "id": "DEPT_HORTICULTURE",
        "name": "Horticulture & Tree Authority",
        "code": "HORT",
        "in_charge": "Superintendent of Gardens & Tree Officer",
        "handles": "Tree debris, fallen trees, uprooted trunks, hanging dangerous branches blocking transit or touching cables",
        "alert_channel": "trees-emergency@municipal.gov.in | VHF Ch-5 | Green Helpline 1099",
        "sla_hours": {"CRITICAL": 2, "HIGH": 5, "MEDIUM": 12, "LOW": 36},
        "keywords": ["tree", "debris", "branch", "uprooted", "trunk", "fallen tree", "foliage", "bough", "timber", "garden", "roots"]
    },
    "DEPT_EMERGENCY_CELL": {
        "id": "DEPT_EMERGENCY_CELL",
        "name": "Municipal Commissioner's Emergency Cell",
        "code": "COMM-CTRL",
        "in_charge": "Additional Municipal Commissioner (Disaster Operations)",
        "handles": "Boundary road jurisdictional disputes, inter-departmental deadlocks, multi-hazard disaster escalations",
        "alert_channel": "commissioner-control@municipal.gov.in | Emergency Control Line 101",
        "sla_hours": {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 4, "LOW": 12},
        "keywords": ["deadlock", "boundary dispute", "emergency", "crisis", "evacuation", "disaster"]
    }
}

# ---------------------------------------------------------------------------
# CORE LOGIC FUNCTIONS
# ---------------------------------------------------------------------------

def classify_hazard_and_route(hazard_type: str, description: str) -> dict:
    """
    Analyzes incident text and categorizes into the appropriate statutory department.
    """
    text = f"{hazard_type} {description}".lower()
    scores = {dept_id: 0 for dept_id in STATUTORY_MUNICIPAL_DEPARTMENTS if dept_id != "DEPT_EMERGENCY_CELL"}

    for dept_id, info in STATUTORY_MUNICIPAL_DEPARTMENTS.items():
        if dept_id == "DEPT_EMERGENCY_CELL":
            continue
        scores[dept_id] = sum(1 for kw in info["keywords"] if kw in text)

    best_dept_id = max(scores, key=scores.get)
    max_matches = scores[best_dept_id]

    problem_map = {
        "DEPT_ELECTRICITY": "Live Wire / Electrical Hazard & Street Lighting",
        "DEPT_DRAINAGE": "Water Clogging & Drainage Issue",
        "DEPT_ROADS": "Road Potholes & Infrastructure Damage",
        "DEPT_HORTICULTURE": "Tree Debris & Transit Obstruction"
    }

    detected_problem = problem_map.get(best_dept_id, "General Municipal Civic Hazard")
    confidence = min(0.99, max(0.70, 0.60 + (max_matches * 0.15)))
    dept_info = STATUTORY_MUNICIPAL_DEPARTMENTS[best_dept_id]

    return {
        "detected_problem": detected_problem,
        "recommended_department_id": best_dept_id,
        "recommended_department_name": dept_info["name"],
        "department_code": dept_info["code"],
        "in_charge_officer": dept_info["in_charge"],
        "alert_channel": dept_info["alert_channel"],
        "confidence": round(confidence, 2)
    }

def compute_urgency_risk_score(hazard_type: str, description: str) -> dict:
    """
    Calculates operational urgency risk score [0 - 100] and priority tier.
    Life-safety hazards (live power wires, open manholes) receive top priority.
    """
    text = f"{hazard_type} {description}".lower()
    score = 75

    if any(k in text for k in ["wire", "shock", "spark", "current", "transformer", "electrocution"]):
        score = 98  # Critical life safety hazard
    elif any(k in text for k in ["manhole", "open drain", "severe flood", "submerged", "drowning"]):
        score = 94
    elif any(k in text for k in ["crater", "uprooted", "cave-in", "blocked road"]):
        score = 88

    priority = "CRITICAL" if score >= 90 else ("HIGH" if score >= 80 else "MEDIUM")
    return {"risk_score": score, "priority": priority}

def calculate_dynamic_sla(dept_id: str, priority: str, custom_hours: Optional[int] = None) -> dict:
    """
    Calculates dynamic resolution deadlines with probabilistic weather-adjusted ranges.
    """
    dept = STATUTORY_MUNICIPAL_DEPARTMENTS.get(dept_id, STATUTORY_MUNICIPAL_DEPARTMENTS["DEPT_DRAINAGE"])
    hrs = custom_hours if custom_hours else dept["sla_hours"].get(priority, 6)
    target = datetime.now(timezone.utc) + timedelta(hours=hrs)
    min_hrs = max(1, int(hrs * 0.75))
    max_hrs = int(hrs * 1.5)

    return {
        "allowed_hours_limit": hrs,
        "sla_target_deadline_utc": target.isoformat(),
        "probabilistic_eta_range": f"{min_hrs} to {max_hrs} hours (subject to monsoon weather severity)"
    }

def detect_ping_pong_deadlock(hops: List[dict]) -> bool:
    """
    Detects if two departments bounced a ticket back and forth on a boundary road.
    e.g. Dept A -> Dept B -> Dept A (Ping-Pong Loop)
    """
    if len(hops) >= 2:
        prev_hop = hops[-2]
        curr_hop = hops[-1]
        if prev_hop["from"] == curr_hop["to"] and prev_hop["to"] == curr_hop["from"]:
            return True
    return False
