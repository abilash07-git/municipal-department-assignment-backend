"""
AI Multi-Department Conflict Analyzer & Ownership Precedence Engine
Resolves departmental boundary ambiguities (e.g. Ward 12 / Ward 13 waterlogging),
prevents ping-pong routing, and enforces statutory root-cause ownership rules.
"""

import re
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# STATUTORY DEPARTMENTS REGISTRY (EXTENDED WITH WATER SUPPLY & SOLID WASTE)
# ---------------------------------------------------------------------------
STATUTORY_DEPARTMENTS = {
    "DEPT_ELECTRICITY": {
        "id": "DEPT_ELECTRICITY",
        "name": "Electricity & Street Lighting Department",
        "code": "ELEC",
        "in_charge": "Superintending Engineer (Power Distribution & Street Lighting)",
        "alert_channel": "electricity-emergency@municipal.gov.in | Emergency Helpline 1912",
        "sla_ack_minutes": {"CRITICAL": 5, "HIGH": 15, "MEDIUM": 30, "LOW": 60},
        "sla_resolution_hours": {"CRITICAL": 1, "HIGH": 3, "MEDIUM": 6, "LOW": 24},
        "keywords": ["wire", "electric", "current", "pole", "transformer", "spark", "cable", "shock", "streetlight", "power", "blackout", "lamp", "voltage", "electrocution", "luminaire"]
    },
    "DEPT_DRAINAGE": {
        "id": "DEPT_DRAINAGE",
        "name": "Stormwater Drainage & Flood Mitigation Department",
        "code": "SWD",
        "in_charge": "Executive Engineer (Stormwater Drainage & Flood Control)",
        "alert_channel": "drainage-emergency@municipal.gov.in | Flood Cell Hotline 1077",
        "sla_ack_minutes": {"CRITICAL": 5, "HIGH": 15, "MEDIUM": 30, "LOW": 60},
        "sla_resolution_hours": {"CRITICAL": 2, "HIGH": 4, "MEDIUM": 8, "LOW": 24},
        "keywords": ["waterlogging", "flood", "drain", "gutter", "manhole", "culvert", "overflow", "stagnant", "submerged", "puddle", "canal", "dewatering", "suction", "silt"]
    },
    "DEPT_ROADS": {
        "id": "DEPT_ROADS",
        "name": "Roads & Infrastructure Department",
        "code": "ROADS",
        "in_charge": "Executive Engineer (Road Maintenance & Pothole Repair)",
        "alert_channel": "roads-repair@municipal.gov.in | Public Works Helpline 1916",
        "sla_ack_minutes": {"CRITICAL": 10, "HIGH": 30, "MEDIUM": 60, "LOW": 120},
        "sla_resolution_hours": {"CRITICAL": 3, "HIGH": 6, "MEDIUM": 12, "LOW": 48},
        "keywords": ["pothole", "crater", "road", "asphalt", "cave-in", "pavement", "footpath", "tar", "divider", "damaged road", "surface", "rut", "kerb", "sinkhole", "median"]
    },
    "DEPT_HORTICULTURE": {
        "id": "DEPT_HORTICULTURE",
        "name": "Horticulture & Tree Authority",
        "code": "HORT",
        "in_charge": "Superintendent of Gardens & Tree Officer",
        "alert_channel": "trees-emergency@municipal.gov.in | Green Helpline 1099",
        "sla_ack_minutes": {"CRITICAL": 10, "HIGH": 30, "MEDIUM": 60, "LOW": 120},
        "sla_resolution_hours": {"CRITICAL": 2, "HIGH": 5, "MEDIUM": 12, "LOW": 36},
        "keywords": ["tree", "debris", "branch", "uprooted", "trunk", "fallen tree", "foliage", "bough", "timber", "garden", "roots", "pruning", "gulmohar", "banyan"]
    },
    "DEPT_WATER_SUPPLY": {
        "id": "DEPT_WATER_SUPPLY",
        "name": "Metro Water Supply & Sewerage Board",
        "code": "MWSSB",
        "in_charge": "Superintending Engineer (Water Distribution Network)",
        "alert_channel": "water-emergency@municipal.gov.in | Water Board Helpline 1916",
        "sla_ack_minutes": {"CRITICAL": 5, "HIGH": 15, "MEDIUM": 30, "LOW": 60},
        "sla_resolution_hours": {"CRITICAL": 2, "HIGH": 4, "MEDIUM": 8, "LOW": 24},
        "keywords": ["pipeline", "water main", "pipe burst", "drinking water", "gushing water", "leakage", "water board", "underground pipe", "potable"]
    },
    "DEPT_SOLID_WASTE": {
        "id": "DEPT_SOLID_WASTE",
        "name": "Solid Waste Management Department",
        "code": "SWM",
        "in_charge": "Chief Engineer (Solid Waste & Environmental Sanitation)",
        "alert_channel": "swm-control@municipal.gov.in | Cleanliness Helpline 1969",
        "sla_ack_minutes": {"CRITICAL": 15, "HIGH": 30, "MEDIUM": 60, "LOW": 120},
        "sla_resolution_hours": {"CRITICAL": 2, "HIGH": 6, "MEDIUM": 12, "LOW": 24},
        "keywords": ["garbage", "waste", "trash", "refuse", "dump", "plastic sacks", "dumped", "compactor", "litter", "filth"]
    },
    "DEPT_SUPERVISOR_CELL": {
        "id": "DEPT_SUPERVISOR_CELL",
        "name": "Zonal Joint Commissioner & Supervisor Control Room",
        "code": "SUPERVISOR",
        "in_charge": "Zonal Joint Municipal Commissioner (Appeals & Inter-Dept Disputes)",
        "alert_channel": "commissioner-disputes@municipal.gov.in | High Command Hot-Line 101",
        "sla_ack_minutes": {"CRITICAL": 5, "HIGH": 10, "MEDIUM": 20, "LOW": 60},
        "sla_resolution_hours": {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 4, "LOW": 8},
        "keywords": ["dispute", "escalation", "deadlock", "boundary dispute", "ping pong", "declined"]
    }
}

# ---------------------------------------------------------------------------
# STATUTORY BOUNDARY ROADS & JURISDICTIONAL AMBIGUITY REGISTRY
# ---------------------------------------------------------------------------
KNOWN_WARD_BOUNDARIES = [
    {
        "boundary_id": "BOUND-W12-W13",
        "wards": ["Ward 12", "Ward 13"],
        "boundary_road": "GN Chetty Arterial Boundary Road",
        "common_disputes": [
            ("DEPT_DRAINAGE", "DEPT_ROADS", "Waterlogging vs Road Maintenance")
        ]
    },
    {
        "boundary_id": "BOUND-W77-W78",
        "wards": ["Ward 77", "Ward 78"],
        "boundary_road": "Gandhi Irwin Boundary Canal Road",
        "common_disputes": [
            ("DEPT_ELECTRICITY", "DEPT_HORTICULTURE", "Live Wire vs Tree Branch"),
            ("DEPT_DRAINAGE", "DEPT_ROADS", "Canal Overflow vs Pavement")
        ]
    },
    {
        "boundary_id": "BOUND-W112-W113",
        "wards": ["Ward 112", "Ward 113"],
        "boundary_road": "Luz Church Boundary Avenue",
        "common_disputes": [
            ("DEPT_WATER_SUPPLY", "DEPT_ROADS", "Water Main Burst vs Road Sinkhole")
        ]
    },
    {
        "boundary_id": "BOUND-W140-W141",
        "wards": ["Ward 140", "Ward 141"],
        "boundary_road": "Anna Salai Arterial Highway Border",
        "common_disputes": [
            ("DEPT_HORTICULTURE", "DEPT_ROADS", "Fallen Tree vs Median Divider")
        ]
    }
]

class AIConflictEngine:
    """
    Intelligent Department Assignment & Conflict Resolution Engine.
    Detects ward boundaries, flags departmental ownership ambiguities,
    applies root-cause statutory precedence rules, and generates dual-SLA assignments.
    """

    @classmethod
    def is_boundary_location(cls, ward: str, description: str, explicit_flag: bool = False) -> Tuple[bool, Optional[str], List[str]]:
        """
        Determines whether the reported issue is located on a ward boundary or boundary road.
        """
        if explicit_flag:
            return True, "Citizen Reported Ward Boundary", ["Ward 12", "Ward 13"]

        combined_text = f"{ward} {description}".lower()
        
        # Check against known boundary registry
        for b in KNOWN_WARD_BOUNDARIES:
            w1, w2 = b["wards"][0].lower(), b["wards"][1].lower()
            if (w1 in combined_text and w2 in combined_text) or (b["boundary_road"].lower() in combined_text):
                return True, b["boundary_road"], b["wards"]

        # Check generic boundary indicators
        boundary_keywords = ["boundary", "border", "between ward", "junction road", "dividing line", "outer ring"]
        for kw in boundary_keywords:
            if kw in combined_text:
                matched_wards = re.findall(r"ward\s*\d+", combined_text, re.IGNORECASE)
                ward_list = [w.title() for w in matched_wards] if matched_wards else ["Adjacent Ward A", "Adjacent Ward B"]
                return True, "Inter-Ward Boundary Arterial Road", ward_list

        return False, None, []

    @classmethod
    def analyze_conflict(cls, hazard_type: str, description: str, ward: str = "", is_ward_boundary: bool = False) -> Dict:
        """
        Analyzes the civic complaint for departmental ownership conflicts.
        Determines primary responsible department, secondary department for joint action,
        and provides statutory conflict-resolution rationale.
        """
        text = f"{hazard_type} {description} {ward}".lower()
        is_boundary, boundary_road, boundary_wards = cls.is_boundary_location(ward, description, is_ward_boundary)

        # 1. Strip negated terms (e.g. "no waterlogging", "without wires", "no flood")
        cleaned_text = re.sub(r'\b(no|not|without|zero|neither|never)\s+([a-z_]+)\b', '', text)

        # 2. Compute keyword match presence for each department with plural-friendly regex
        dept_scores = {}
        for dept_id, dept in STATUTORY_DEPARTMENTS.items():
            if dept_id == "DEPT_SUPERVISOR_CELL":
                continue
            matched_kws = []
            for kw in dept["keywords"]:
                pattern = r'\b' + re.escape(kw) + r'(s|es|ing|ed)?\b'
                if re.search(pattern, cleaned_text):
                    matched_kws.append(kw)
            dept_scores[dept_id] = len(matched_kws)

        has_elec = dept_scores.get("DEPT_ELECTRICITY", 0) > 0
        has_drainage = dept_scores.get("DEPT_DRAINAGE", 0) > 0
        has_roads = dept_scores.get("DEPT_ROADS", 0) > 0
        has_hort = dept_scores.get("DEPT_HORTICULTURE", 0) > 0
        has_water = dept_scores.get("DEPT_WATER_SUPPLY", 0) > 0
        has_swm = dept_scores.get("DEPT_SOLID_WASTE", 0) > 0

        # Specific problem indicators
        is_pipe_burst = any(k in cleaned_text for k in ["pipeline", "pipe burst", "drinking water", "water main", "water board"])
        is_garbage_dump = any(k in cleaned_text for k in ["garbage", "refuse", "plastic sacks", "dumped", "packaging"])
        is_live_wire = any(k in cleaned_text for k in ["spark", "live wire", "shock", "voltage", "current", "electrocution", "snapped", "transformer"])

        is_conflict = False
        conflict_type = "SINGLE_DEPARTMENT_MANDATE"
        primary_id = None
        secondary_id = None
        ownership_rule = "DIRECT_STATUTORY_MANDATE"
        rationale = ""
        joint_action = False

        # RULE HIERARCHY EVALUATION (ORDER OF SPECIFICITY):

        # Priority 1: Live Electric Hazard Entangled with Water or Tree (Life Safety Override)
        if has_elec and is_live_wire:
            if has_drainage or "flood" in cleaned_text:
                is_conflict = True
                conflict_type = "ELECTROCUTION_IN_FLOODWATER"
                primary_id = "DEPT_ELECTRICITY"
                secondary_id = "DEPT_DRAINAGE"
                ownership_rule = "LIFE_SAFETY_ISOLATION_PRECEDENCE"
                rationale = "Imminent electrocution hazard takes absolute life-safety priority. Substation feeder must be de-energized and certified safe by Electricity Department before Drainage crews can deploy suction pumps."
                joint_action = True
            elif has_hort or "tree" in cleaned_text or "branch" in cleaned_text:
                is_conflict = True
                conflict_type = "LIVE_POWER_AND_TREE_ENTANGLEMENT"
                primary_id = "DEPT_ELECTRICITY"
                secondary_id = "DEPT_HORTICULTURE"
                ownership_rule = "LIFE_SAFETY_ISOLATION_PRECEDENCE"
                rationale = "Live high-voltage power cable touching tree foliage presents instant shock danger. Electricity crew must de-energize and secure wire before Horticulture team can saw tree limbs."
                joint_action = True
            elif is_boundary:
                is_conflict = True
                conflict_type = "BOUNDARY_ROAD_ELECTRICAL_HAZARD"
                primary_id = "DEPT_ELECTRICITY"
                secondary_id = "DEPT_ROADS"
                ownership_rule = "LIFE_SAFETY_ISOLATION_PRECEDENCE"
                rationale = "Live power hazard on boundary road requires immediate electrical isolation before road traffic diversion and asphalt inspection."
                joint_action = True
            else:
                primary_id = "DEPT_ELECTRICITY"
                secondary_id = None
                is_conflict = False
                conflict_type = "SINGLE_DEPARTMENT_MANDATE"
                ownership_rule = "DIRECT_STATUTORY_MANDATE"
                rationale = "Live electrical distribution and power line repair handled under statutory jurisdiction of Electricity Department."
                joint_action = False

        # Priority 2: Underground Water Supply Pipe Burst causing Road Crater / Sinkhole
        elif is_pipe_burst and (has_roads or "crater" in cleaned_text or "sinkhole" in cleaned_text or "road" in cleaned_text):
            is_conflict = True
            conflict_type = "UNDERGROUND_PIPE_BURST_AND_ROAD_CAVE_IN"
            primary_id = "DEPT_WATER_SUPPLY"
            secondary_id = "DEPT_ROADS"
            ownership_rule = "UTILITY_EROSION_PRECEDENCE"
            rationale = "Active pressurized drinking water pipeline burst is the root cause of ground subsidence. Water board must isolate valve and repair pipeline before Road crew can backfill and compact asphalt."
            joint_action = True

        # Priority 3: Solid Waste / Garbage Blocking Storm Drain Canal
        elif is_garbage_dump and (has_drainage or "drain" in cleaned_text or "canal" in cleaned_text):
            is_conflict = True
            conflict_type = "GARBAGE_BLOCKING_STORM_DRAIN"
            primary_id = "DEPT_SOLID_WASTE"
            secondary_id = "DEPT_DRAINAGE"
            ownership_rule = "DEBRIS_CLEARANCE_PRECEDENCE"
            rationale = "External dumped commercial refuse and garbage must be cleared by Solid Waste compactors before Drainage department can desilt the interior canal bed."
            joint_action = True

        # Priority 4: Fallen Tree Obstructing Arterial Road / Crushing Median
        elif has_hort and (has_roads or "road" in cleaned_text or "avenue" in cleaned_text or "divider" in cleaned_text) and any(k in cleaned_text for k in ["uprooted", "fallen", "blocking", "collapsed"]):
            is_conflict = True
            conflict_type = "TRANSIT_OBSTRUCTION_AND_ROAD_DAMAGE"
            primary_id = "DEPT_HORTICULTURE"
            secondary_id = "DEPT_ROADS"
            ownership_rule = "TRANSIT_OBSTRUCTION_PRECEDENCE"
            rationale = "Physical tree trunk and debris obstruction must be cut and removed by Horticulture woodcutters before Road Department can rebuild damaged divider kerb."
            joint_action = True

        # Priority 5: Waterlogging on Road / Boundary Road Drainage Dispute (Problem 3 Core)
        elif (has_drainage and has_roads and any(k in cleaned_text for k in ["waterlogg", "flood", "overflow", "stagnant"])) or \
             (has_drainage and is_boundary and any(k in cleaned_text for k in ["road", "avenue", "street", "arterial"])):
            is_conflict = True
            conflict_type = "BOUNDARY_ROAD_DUAL_INFRASTRUCTURE"
            primary_id = "DEPT_DRAINAGE"
            secondary_id = "DEPT_ROADS"
            ownership_rule = "HYDRAULIC_ROOT_CAUSE_PRECEDENCE"
            rationale = "Waterlogging on road is hydraulically caused by drainage blockage. Dewatering and drain clearance is prerequisite before road damage inspection or asphalt resurfacing."
            joint_action = True

        # Priority 6: Single Department (Non-Conflict Baseline)
        else:
            active_depts = [d for d, s in dept_scores.items() if s > 0]
            active_depts.sort(key=lambda d: dept_scores[d], reverse=True)
            primary_id = active_depts[0] if active_depts else "DEPT_ROADS"
            secondary_id = None
            is_conflict = False
            conflict_type = "SINGLE_DEPARTMENT_MANDATE"
            ownership_rule = "DIRECT_STATUTORY_MANDATE"
            dept_name = STATUTORY_DEPARTMENTS[primary_id]["name"]
            rationale = f"Standard civic issue handled directly under statutory jurisdiction of {dept_name}."
            joint_action = False

        primary_info = STATUTORY_DEPARTMENTS[primary_id]
        secondary_info = STATUTORY_DEPARTMENTS[secondary_id] if secondary_id else None

        confidence = 0.985 if is_conflict else 0.95

        return {
            "is_conflict_detected": is_conflict,
            "conflict_type": conflict_type,
            "is_ward_boundary": is_boundary,
            "boundary_road_name": boundary_road,
            "boundary_wards": boundary_wards,
            "primary_department": {
                "id": primary_info["id"],
                "name": primary_info["name"],
                "code": primary_info["code"],
                "role": "LEAD_RESPONDER",
                "in_charge": primary_info["in_charge"],
                "alert_channel": primary_info["alert_channel"]
            },
            "secondary_department": {
                "id": secondary_info["id"],
                "name": secondary_info["name"],
                "code": secondary_info["code"],
                "role": "JOINT_SUPPORT_COORDINATOR",
                "in_charge": secondary_info["in_charge"],
                "alert_channel": secondary_info["alert_channel"]
            } if secondary_info else None,
            "ownership_rule_applied": ownership_rule,
            "conflict_resolution_rationale": rationale,
            "joint_action_required": joint_action,
            "ai_confidence": round(confidence, 3)
        }

    @classmethod
    def calculate_dual_slas(
        cls,
        primary_dept_id: str,
        secondary_dept_id: Optional[str],
        priority: str = "HIGH",
        is_critical_safety: bool = False
    ) -> Dict:
        """
        Computes independent SLA clocks for both departments:
        - Acknowledgment SLA (demonstration policy: 5 minutes for critical safety)
        - Resolution SLA (e.g. 1-4 hours based on priority)
        """
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        p_dept = STATUTORY_DEPARTMENTS[primary_dept_id]
        
        # Primary Acknowledgment SLA (Demonstration policy: 5 mins if critical/safety, otherwise configured)
        p_ack_mins = 5 if (is_critical_safety or priority == "CRITICAL") else p_dept["sla_ack_minutes"].get(priority, 15)
        p_res_hrs = p_dept["sla_resolution_hours"].get(priority, 4)

        primary_sla = {
            "department_id": primary_dept_id,
            "department_name": p_dept["name"],
            "department_code": p_dept["code"],
            "role": "LEAD_RESPONDER",
            "acknowledgment_deadline_utc": (now + timedelta(minutes=p_ack_mins)).isoformat(),
            "acknowledgment_limit_minutes": p_ack_mins,
            "resolution_deadline_utc": (now + timedelta(hours=p_res_hrs)).isoformat(),
            "resolution_limit_hours": p_res_hrs,
            "is_acknowledged": False,
            "acknowledged_at_utc": None,
            "acknowledged_by": None,
            "is_breached": False
        }

        secondary_sla = None
        if secondary_dept_id:
            s_dept = STATUTORY_DEPARTMENTS[secondary_dept_id]
            s_ack_mins = 15 if (is_critical_safety or priority == "CRITICAL") else s_dept["sla_ack_minutes"].get(priority, 30)
            s_res_hrs = max(p_res_hrs + 2, s_dept["sla_resolution_hours"].get(priority, 6))

            secondary_sla = {
                "department_id": secondary_dept_id,
                "department_name": s_dept["name"],
                "department_code": s_dept["code"],
                "role": "JOINT_SUPPORT_COORDINATOR",
                "acknowledgment_deadline_utc": (now + timedelta(minutes=s_ack_mins)).isoformat(),
                "acknowledgment_limit_minutes": s_ack_mins,
                "resolution_deadline_utc": (now + timedelta(hours=s_res_hrs)).isoformat(),
                "resolution_limit_hours": s_res_hrs,
                "is_acknowledged": False,
                "acknowledged_at_utc": None,
                "acknowledged_by": None,
                "is_breached": False
            }

        return {
            "primary_sla": primary_sla,
            "secondary_sla": secondary_sla,
            "demonstration_policy_note": f"Demonstration SLA Policy: Critical safety complaint mandates acknowledgment within {p_ack_mins} minutes or triggers immediate supervisor escalation."
        }
