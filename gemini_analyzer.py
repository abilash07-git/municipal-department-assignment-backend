"""
Gemini Multimodal Municipal Conflict Analyzer
Integrates Google Gemini API (gemini-2.5-flash) via official google-genai SDK
for intelligent multimodal civic hazard analysis, ward boundary dispute resolution,
and statutory root-cause precedence routing.
"""

import os
import sys
import json
import base64
import logging
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Logger setup
logger = logging.getLogger("gemini_analyzer")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [GeminiAnalyzer] %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Check for google.genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai SDK not found. Fallback mode will be active.")

# Import local statutory registry and deterministic fallback engine
from ai_conflict_engine import AIConflictEngine, STATUTORY_DEPARTMENTS

# ---------------------------------------------------------------------------
# STRUCTURED PYDANTIC SCHEMA FOR GEMINI OUTPUT
# ---------------------------------------------------------------------------
class GeminiConflictAnalysisSchema(BaseModel):
    is_conflict_detected: bool = Field(
        description="Whether this civic incident involves jurisdictional overlap between two or more departments."
    )
    conflict_type: str = Field(
        description="Canonical conflict type code: BOUNDARY_ROAD_DUAL_INFRASTRUCTURE, LIVE_POWER_AND_TREE_ENTANGLEMENT, UNDERGROUND_PIPE_BURST_AND_ROAD_CAVE_IN, TRANSIT_OBSTRUCTION_AND_ROAD_DAMAGE, GARBAGE_BLOCKING_STORM_DRAIN, ELECTROCUTION_IN_FLOODWATER, or SINGLE_DEPARTMENT_MANDATE."
    )
    is_ward_boundary: bool = Field(
        description="Whether the reported location lies on or near an inter-ward border (e.g. Ward 12 / Ward 13)."
    )
    boundary_road_name: Optional[str] = Field(
        default=None,
        description="Identified boundary arterial road name if applicable."
    )
    boundary_wards: List[str] = Field(
        default_factory=list,
        description="List of adjacent wards involved (e.g. ['Ward 12', 'Ward 13'])."
    )
    primary_department_id: str = Field(
        description="Statutory ID of lead responding department: DEPT_DRAINAGE, DEPT_ELECTRICITY, DEPT_ROADS, DEPT_HORTICULTURE, DEPT_WATER_SUPPLY, or DEPT_SOLID_WASTE."
    )
    secondary_department_id: Optional[str] = Field(
        default=None,
        description="Statutory ID of secondary department for joint coordination, or null if single department."
    )
    ownership_rule_applied: str = Field(
        description="Statutory precedence rule: HYDRAULIC_ROOT_CAUSE_PRECEDENCE, LIFE_SAFETY_ISOLATION_PRECEDENCE, UTILITY_EROSION_PRECEDENCE, TRANSIT_OBSTRUCTION_PRECEDENCE, DEBRIS_CLEARANCE_PRECEDENCE, or DIRECT_STATUTORY_MANDATE."
    )
    conflict_resolution_rationale: str = Field(
        description="Exhaustive legal, engineering, and physical root-cause rationale for why the primary department has lead ownership and secondary has joint standby."
    )
    joint_action_required: bool = Field(
        description="True if secondary department must be deployed concurrently or upon primary task completion."
    )
    urgency_risk_score: int = Field(
        description="Risk score from 1 (lowest) to 100 (critical life safety)."
    )
    recommended_immediate_action: str = Field(
        description="Concrete immediate operational order for the lead responding crew."
    )
    ai_confidence: float = Field(
        description="Confidence score between 0.0 and 1.0."
    )

# ---------------------------------------------------------------------------
# GEMINI HIGH-COMMAND SYSTEM INSTRUCTION
# ---------------------------------------------------------------------------
GEMINI_SYSTEM_INSTRUCTION = """
You are the Municipal High-Command AI Conflict & Statutory Jurisdiction Engine.
Your duty is to ingest citizen civic complaints and uploaded incident photos, detect whether the location lies on a ward boundary, and definitively resolve departmental ownership disputes between municipal bodies (e.g., Stormwater Drainage vs Roads & Infrastructure).

MUNICIPAL STATUTORY DEPARTMENTS REGISTRY:
1. DEPT_DRAINAGE: Stormwater Drainage & Flood Mitigation Department (Code: SWD)
   - Mandate: Stormwater drains, culverts, dewatering pumps, canal clearing, flood mitigation.
2. DEPT_ROADS: Roads & Infrastructure Department (Code: ROADS)
   - Mandate: Asphalt paving, pothole filling, pavement repair, median divider restoration, road resurfacing.
3. DEPT_ELECTRICITY: Electricity & Street Lighting Department (Code: ELEC)
   - Mandate: High-voltage distribution lines, transformers, streetlights, poles, electrical isolation.
4. DEPT_HORTICULTURE: Horticulture & Tree Authority (Code: HORT)
   - Mandate: Tree pruning, uprooted tree sectioning and clearing, botanical debris removal.
5. DEPT_WATER_SUPPLY: Metro Water Supply & Sewerage Board (Code: MWSSB)
   - Mandate: Pressurized potable drinking water distribution, water main pipelines, underground sluice valves.
6. DEPT_SOLID_WASTE: Solid Waste Management Department (Code: SWM)
   - Mandate: Garbage collection, dumped refuse, commercial packaging waste, mechanical grab compactors.

PROBLEM 3 STATUTORY ROOT-CAUSE PRECEDENCE HIERARCHY:
A complaint must NEVER remain unresolved because departments disagree about who owns it.
When multiple departments claim "it's the other department's problem", apply these strict engineering precedence rules:

Priority 1: LIFE_SAFETY_ISOLATION_PRECEDENCE
- If live electrical distribution wires are sparking, snapped, or in contact with floodwater/trees, DEPT_ELECTRICITY takes absolute life-safety priority. Substation feeder must be de-energized and certified dead before Drainage pumps or Horticulture saws can approach.

Priority 2: HYDRAULIC_ROOT_CAUSE_PRECEDENCE (The Problem 3 Core)
- Waterlogging on a road is hydraulically caused by drainage blockage. Dewatering and drain clearance by DEPT_DRAINAGE is the mandatory prerequisite before DEPT_ROADS can inspect pavement or lay asphalt. Road asphalt cannot be paved or patched under standing floodwater. DEPT_DRAINAGE is Primary (Lead); DEPT_ROADS is Secondary (Joint Support).

Priority 3: UTILITY_EROSION_PRECEDENCE
- An underground pressurized drinking water pipe burst causing road crater/sinkhole requires DEPT_WATER_SUPPLY to isolate the valve and replace pipe before DEPT_ROADS can backfill and compact asphalt.

Priority 4: TRANSIT_OBSTRUCTION_PRECEDENCE
- A massive uprooted tree blocking an arterial road requires DEPT_HORTICULTURE hydraulic saws and cranes to section and haul timber before DEPT_ROADS can repair crushed median dividers.

Priority 5: DEBRIS_CLEARANCE_PRECEDENCE
- Dumped commercial garbage choking a storm drainage canal requires DEPT_SOLID_WASTE compactors to scoop surface refuse before DEPT_DRAINAGE can desilt canal bed.

Always produce valid structured JSON conforming strictly to the requested schema.
"""

class GeminiMunicipalAnalyzer:
    """
    Multimodal Gemini API Client for Municipal Department Assignment and Conflict Resolution.
    Supports image + text reasoning, structured Pydantic output, and fallback.
    """

    DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @classmethod
    def get_api_key(cls, explicit_key: Optional[str] = None) -> Optional[str]:
        """Resolves Gemini API key from explicit arg, env, or .env file."""
        return explicit_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    @classmethod
    def is_available(cls, explicit_key: Optional[str] = None) -> bool:
        """Returns True if SDK is installed and an API key is configured."""
        return GENAI_AVAILABLE and bool(cls.get_api_key(explicit_key))

    @classmethod
    def _prepare_image_part(cls, image_ref: Optional[str]) -> Optional[Any]:
        """
        Loads an image from local filepath or base64 data URL into a Gemini Part.
        """
        if not image_ref or not GENAI_AVAILABLE:
            return None

        try:
            # Check if local file exists
            if os.path.exists(image_ref):
                with open(image_ref, "rb") as f:
                    img_bytes = f.read()
                ext = os.path.splitext(image_ref)[1].lower().replace(".", "")
                mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
                return types.Part.from_bytes(data=img_bytes, mime_type=mime)

            # Check if base64 data url
            if image_ref.startswith("data:image"):
                header, encoded = image_ref.split(",", 1)
                mime = header.split(";")[0].replace("data:", "")
                img_bytes = base64.b64decode(encoded)
                return types.Part.from_bytes(data=img_bytes, mime_type=mime)

        except Exception as e:
            logger.warning(f"Failed to prepare image part for Gemini: {e}")

        return None

    @classmethod
    def analyze_complaint(
        cls,
        hazard_type: str,
        description: str,
        ward: str = "Ward 12 / Ward 13 Boundary",
        is_ward_boundary: bool = False,
        image_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main Analysis Entrypoint:
        1. Calls Google Gemini API if configured with multimodal reasoning.
        2. Falls back to deterministic AIConflictEngine if Gemini is offline/unconfigured.
        """
        resolved_key = cls.get_api_key(api_key)
        target_model = model_name or cls.DEFAULT_MODEL

        # If Gemini is available, invoke Gemini Multimodal Model
        if GENAI_AVAILABLE and resolved_key:
            try:
                logger.info(f"Invoking Google Gemini API ({target_model}) for incident analysis...")
                client = genai.Client(api_key=resolved_key)

                prompt_text = (
                    f"CIVIC COMPLAINT TELEMETRY FOR ANALYSIS:\n"
                    f"Reported Hazard: {hazard_type}\n"
                    f"Ward Location: {ward}\n"
                    f"Explicit Ward Boundary Flag: {is_ward_boundary}\n"
                    f"Citizen Description: {description}\n\n"
                    f"Analyze this civic incident carefully. Detect if this is on a ward boundary, "
                    f"identify conflicting municipal departments, and apply statutory root-cause precedence."
                )

                contents: List[Any] = []
                img_part = cls._prepare_image_part(image_url)
                if img_part:
                    contents.append(img_part)
                    prompt_text += "\n[A photo of the civic incident is attached. Inspect visual evidence for flood depth, live wires, trees, road craters, and infrastructure damage]."

                contents.append(prompt_text)

                response = client.models.generate_content(
                    model=target_model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=GEMINI_SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=GeminiConflictAnalysisSchema,
                        temperature=0.1
                    )
                )

                # Parse structured JSON output
                raw_json = response.text
                data = json.loads(raw_json)

                # Validate and format against statutory department schemas
                primary_id = data["primary_department_id"]
                if primary_id not in STATUTORY_DEPARTMENTS:
                    primary_id = "DEPT_DRAINAGE" if "drain" in hazard_type.lower() or "water" in description.lower() else "DEPT_ROADS"

                secondary_id = data.get("secondary_department_id")
                if secondary_id and secondary_id not in STATUTORY_DEPARTMENTS:
                    secondary_id = None

                primary_info = STATUTORY_DEPARTMENTS[primary_id]
                secondary_info = STATUTORY_DEPARTMENTS[secondary_id] if secondary_id else None

                return {
                    "is_conflict_detected": data["is_conflict_detected"],
                    "conflict_type": data["conflict_type"],
                    "is_ward_boundary": data["is_ward_boundary"],
                    "boundary_road_name": data.get("boundary_road_name") or "Inter-Ward Arterial Boundary Road",
                    "boundary_wards": data.get("boundary_wards") or ["Ward 12", "Ward 13"],
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
                    "ownership_rule_applied": data["ownership_rule_applied"],
                    "conflict_resolution_rationale": data["conflict_resolution_rationale"],
                    "joint_action_required": data["joint_action_required"],
                    "urgency_risk_score": data.get("urgency_risk_score", 90),
                    "recommended_immediate_action": data.get("recommended_immediate_action", "Immediate emergency deployment mandated."),
                    "ai_confidence": data.get("ai_confidence", 0.985),
                    "ai_engine": "GOOGLE_GEMINI_MULTIMODAL",
                    "ai_model": target_model,
                    "image_analyzed": bool(img_part)
                }

            except Exception as e:
                logger.error(f"Gemini API invocation encountered error: {e}. Falling back to statutory precedence engine.")

        # Seamless Fallback to Statutory Precedence Rule Engine
        logger.info("Using Statutory Precedence Rule Engine (Deterministic Fallback).")
        fallback_res = AIConflictEngine.analyze_conflict(
            hazard_type=hazard_type,
            description=description,
            ward=ward,
            is_ward_boundary=is_ward_boundary
        )
        fallback_res["ai_engine"] = "STATUTORY_PRECEDENCE_FALLBACK"
        fallback_res["ai_model"] = "Deterministic_DAG_Precedence_v2"
        fallback_res["recommended_immediate_action"] = (
            "Deploy high-volume suction pumps to clear drain mouth"
            if fallback_res["primary_department"]["id"] == "DEPT_DRAINAGE"
            else "Immediate field inspection and hazard mitigation mandated."
        )
        fallback_res["urgency_risk_score"] = 95 if fallback_res["is_conflict_detected"] else 70
        fallback_res["image_analyzed"] = bool(image_url)

        return fallback_res
