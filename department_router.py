"""
Statutory Municipal Department Routing & Conflict Resolution Engine
Provides automated problem classification, boundary dispute resolution,
dual-department pre-routing, dynamic SLA clocks, and anti-ping-pong interceptor.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone
from ai_conflict_engine import STATUTORY_DEPARTMENTS, AIConflictEngine

STATUTORY_MUNICIPAL_DEPARTMENTS = STATUTORY_DEPARTMENTS

def classify_hazard_and_route(hazard_type: str, description: str, ward: str = "", is_ward_boundary: bool = False) -> dict:
    """
    Analyzes incident text, detects ward boundary ambiguities,
    applies root-cause statutory precedence rules, and routes to primary and secondary departments.
    """
    conflict_res = AIConflictEngine.analyze_conflict(
        hazard_type=hazard_type,
        description=description,
        ward=ward,
        is_ward_boundary=is_ward_boundary
    )

    problem_map = {
        "DEPT_ELECTRICITY": "Live Wire / Electrical Hazard & Street Lighting",
        "DEPT_DRAINAGE": "Water Clogging & Drainage Issue",
        "DEPT_ROADS": "Road Potholes & Infrastructure Damage",
        "DEPT_HORTICULTURE": "Tree Debris & Transit Obstruction",
        "DEPT_WATER_SUPPLY": "Water Main Burst & Utility Subsidence",
        "DEPT_SOLID_WASTE": "Commercial Solid Waste Dump & SWM Overflow"
    }

    primary_id = conflict_res["primary_department"]["id"]
    detected_problem = problem_map.get(primary_id, "General Municipal Civic Hazard")

    return {
        "detected_problem": detected_problem,
        "is_conflict_detected": conflict_res["is_conflict_detected"],
        "conflict_type": conflict_res["conflict_type"],
        "is_ward_boundary": conflict_res["is_ward_boundary"],
        "boundary_road_name": conflict_res["boundary_road_name"],
        "boundary_wards": conflict_res["boundary_wards"],
        "primary_department": conflict_res["primary_department"],
        "secondary_department": conflict_res["secondary_department"],
        "ownership_rule_applied": conflict_res["ownership_rule_applied"],
        "conflict_resolution_rationale": conflict_res["conflict_resolution_rationale"],
        "joint_action_required": conflict_res["joint_action_required"],
        "confidence": conflict_res["ai_confidence"]
    }

def compute_urgency_risk_score(hazard_type: str, description: str, is_conflict: bool = False) -> dict:
    """
    Calculates operational urgency risk score [0 - 100] and priority tier.
    Life-safety hazards (live power wires, open manholes) receive top priority.
    Boundary multi-department conflicts receive an urgency uplift to prevent delays.
    """
    text = f"{hazard_type} {description}".lower()
    score = 75

    if any(k in text for k in ["wire", "shock", "spark", "current", "transformer", "electrocution"]):
        score = 98  # Critical life safety hazard
    elif any(k in text for k in ["manhole", "open drain", "severe flood", "submerged", "drowning", "knee deep"]):
        score = 95
    elif any(k in text for k in ["pipe burst", "sinkhole", "crater", "uprooted", "cave-in", "blocked road"]):
        score = 90
    elif is_conflict:
        score = 88  # Priority boost for boundary disputes

    priority = "CRITICAL" if score >= 90 else ("HIGH" if score >= 80 else "MEDIUM")
    return {"risk_score": score, "priority": priority}

def calculate_dual_slas(primary_dept_id: str, secondary_dept_id: Optional[str] = None, priority: str = "HIGH") -> dict:
    """
    Calculates dual independent SLA clocks (Acknowledgment SLA + Resolution SLA) for both departments.
    Enforces the demonstration policy: critical safety complaints require acknowledgment within 5 minutes.
    """
    return AIConflictEngine.calculate_dual_slas(
        primary_dept_id=primary_dept_id,
        secondary_dept_id=secondary_dept_id,
        priority=priority,
        is_critical_safety=(priority == "CRITICAL")
    )

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in meters."""
    from math import radians, cos, sin, asin, sqrt
    R = 6371000.0  # Earth radius in meters
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2.0) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2.0) ** 2
    c = 2.0 * asin(sqrt(a))
    return R * c

def cluster_complaints_by_proximity(complaints: List[dict], max_distance_meters: float = 80.0) -> List[dict]:
    """
    Groups overlapping citizen reports by location radius (<= 80m) and department type.
    Prevents dispatching duplicate crews to the exact same incident during storms.
    """
    clusters = []
    visited = set()

    for i, c1 in enumerate(complaints):
        if c1["complaint_id"] in visited:
            continue

        c1_lat = c1["coordinates"]["latitude"]
        c1_lon = c1["coordinates"]["longitude"]
        dept1 = c1.get("primary_department", {}).get("id") or c1.get("assigned_department")

        cluster_members = [c1]
        visited.add(c1["complaint_id"])

        for j, c2 in enumerate(complaints):
            if c2["complaint_id"] in visited:
                continue

            dept2 = c2.get("primary_department", {}).get("id") or c2.get("assigned_department")
            if dept1 != dept2:
                continue

            c2_lat = c2["coordinates"]["latitude"]
            c2_lon = c2["coordinates"]["longitude"]
            dist = haversine_distance_meters(c1_lat, c1_lon, c2_lat, c2_lon)

            if dist <= max_distance_meters:
                cluster_members.append(c2)
                visited.add(c2["complaint_id"])

        lead_complaint = max(cluster_members, key=lambda x: x.get("risk_score", 50))
        p_dept = lead_complaint.get("primary_department", {})
        clusters.append({
            "cluster_id": f"CLUST-{lead_complaint['complaint_id'].replace('CMP-', '')}",
            "lead_complaint_id": lead_complaint["complaint_id"],
            "detected_problem": lead_complaint["detected_problem"],
            "department_id": dept1,
            "department_name": p_dept.get("name", "Municipal Department"),
            "highest_risk_score": lead_complaint["risk_score"],
            "total_citizen_reports": len(cluster_members),
            "approximate_location": {
                "latitude": round(sum(m["coordinates"]["latitude"] for m in cluster_members) / len(cluster_members), 4),
                "longitude": round(sum(m["coordinates"]["longitude"] for m in cluster_members) / len(cluster_members), 4)
            },
            "member_complaints": [m["complaint_id"] for m in cluster_members]
        })

    return clusters
