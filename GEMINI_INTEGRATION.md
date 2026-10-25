# 🤖 Google Gemini API Multimodal Integration & Conflict Resolution

This document details the Google Gemini API integration within the `municipal-department-assignment-backend` engine.

---

## 📌 Executive Overview

The **Problem 3 Challenge** requires resolving jurisdictional boundary ambiguities when two municipal departments dispute ticket ownership (e.g., Ward 12 & 13 waterlogged road: Stormwater Drainage vs Roads Department).

By integrating the **Google Gemini API** (`google-genai` SDK) with **`gemini-2.5-flash`**, the platform delivers:
1. **Multimodal Incident Reasoning:** Concurrently inspects citizen complaint text, geo-coordinates, and **uploaded incident photos** (flood levels, live wires, uprooted trees, pipe bursts, debris).
2. **AI Statutory Precedence Resolution:** Leverages deep reasoning to definitively determine physical root causes and assign the **Lead Responding Department** and **Joint Support Coordinator**.
3. **Structured Pydantic Outputs:** Strictly outputs typed JSON conforming to municipal schemas via Gemini's native `response_schema` feature.
4. **Zero-Downtime Fallback:** If `GEMINI_API_KEY` is not configured, or if an offline test occurs, the system smoothly falls back to the deterministic DAG precedence engine with 100% reliability.

---

## 🏛️ System Architecture

```
[Citizen Ingests Complaint + Incident Photo]
                      │
                      ▼
         [GeminiMunicipalAnalyzer]
                      │
         ┌────────────┴────────────┐
         │ Is GEMINI_API_KEY Set?  │
         └────────────┬────────────┘
               YES    │    NO / Error
       ┌──────────────┴──────────────┐
       ▼                             ▼
[Google Gemini 2.5 Flash]     [Deterministic DAG Fallback]
• Multimodal Image Inspection • Statutory Precedence DAG
• Root-Cause Reasoning        • Sub-millisecond Execution
• Structured Pydantic Output  • 100% Offline Accuracy
       └──────────────┬──────────────┘
                      │
                      ▼
     [Unified Conflict Telemetry]
     • Primary Department (Lead Responder)
     • Secondary Department (Joint Support)
     • Precedence Rule Applied & Engineering Rationale
     • Dual Independent SLA Clocks (5-Min Ack Policy)
     • Anti-Ping-Pong Dispute Lock
```

---

## ⚙️ Quick Start & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Includes `google-genai>=2.30.0` and `python-dotenv>=1.0.0`).*

### 2. Configure Your API Key
Copy the example environment file and add your Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/):

```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
GEMINI_MODEL=gemini-2.5-flash
```

> **Note on Zero-Downtime Fallback:**
> If `GEMINI_API_KEY` is omitted, the engine automatically runs in `STATUTORY_PRECEDENCE_FALLBACK` mode. You do **not** need a key to run local unit tests or integration simulations!

---

## 📡 API Endpoints Reference

### 1. Check Gemini Operational Status
```http
GET /api/v1/gemini/status
```

#### Sample Response:
```json
{
  "gemini_sdk_installed": true,
  "gemini_api_key_configured": true,
  "configured_model": "gemini-2.5-flash",
  "active_engine": "GOOGLE_GEMINI_MULTIMODAL",
  "zero_downtime_fallback_active": true,
  "instructions": "Set GEMINI_API_KEY in .env or environment to enable live Gemini multimodal reasoning."
}
```

---

### 2. Direct Gemini Multimodal Analysis Endpoint
```http
POST /api/v1/gemini/analyze
Content-Type: application/json
```

#### Request Payload:
```json
{
  "hazard_type": "WATERLOGGING_ROAD",
  "description": "Heavy rainfall causes severe waterlogging on GN Chetty Road between Ward 12 and Ward 13. Multiple cars submerged, drainage inlet choked.",
  "ward": "Ward 12 / Ward 13 Boundary",
  "is_ward_boundary": true,
  "image_url": "chennai_monsoon_raw.jpg"
}
```

#### Structured Response (from Gemini):
```json
{
  "is_conflict_detected": true,
  "conflict_type": "BOUNDARY_ROAD_DUAL_INFRASTRUCTURE",
  "is_ward_boundary": true,
  "boundary_road_name": "GN Chetty Arterial Boundary Road",
  "boundary_wards": ["Ward 12", "Ward 13"],
  "primary_department": {
    "id": "DEPT_DRAINAGE",
    "name": "Stormwater Drainage & Flood Mitigation Department",
    "code": "SWD",
    "role": "LEAD_RESPONDER",
    "in_charge": "Executive Engineer (Stormwater Drainage & Flood Control)",
    "alert_channel": "drainage-emergency@municipal.gov.in | Flood Cell Hotline 1077"
  },
  "secondary_department": {
    "id": "DEPT_ROADS",
    "name": "Roads & Infrastructure Department",
    "code": "ROADS",
    "role": "JOINT_SUPPORT_COORDINATOR",
    "in_charge": "Executive Engineer (Road Maintenance & Pothole Repair)",
    "alert_channel": "roads-repair@municipal.gov.in | Public Works Helpline 1916"
  },
  "ownership_rule_applied": "HYDRAULIC_ROOT_CAUSE_PRECEDENCE",
  "conflict_resolution_rationale": "Waterlogging on road is hydraulically caused by drainage blockage. Dewatering and drain clearance is prerequisite before road damage inspection or asphalt resurfacing.",
  "joint_action_required": true,
  "urgency_risk_score": 95,
  "recommended_immediate_action": "Deploy high-capacity suction pumps to clear drain mouth and dewater carriageway.",
  "ai_confidence": 0.985,
  "ai_engine": "GOOGLE_GEMINI_MULTIMODAL",
  "ai_model": "gemini-2.5-flash",
  "image_analyzed": true
}
```

---

### 3. Register Civic Complaint (Main Workflow)
```http
POST /api/v1/complaints
Content-Type: application/json
```
Ingests complaint, runs Gemini reasoning (or fallback), launches Dual SLAs, and pre-selects primary owner.

---

## ⚖️ Precedence Hierarchy Enforced by Gemini

| Priority Tier | Precedence Rule | Conflict Scenario | Lead Department (Primary) | Secondary (Joint) | Core Engineering Rationale |
|---|---|---|---|---|---|
| **Priority 1** | `LIFE_SAFETY_ISOLATION_PRECEDENCE` | Live wire sparking in floodwater or touching tree limbs | **Electricity (`ELEC`)** | **Drainage / Horticulture** | Imminent electrocution hazard takes absolute life-safety priority. Feeder must be de-energized before other crews approach. |
| **Priority 2** | `HYDRAULIC_ROOT_CAUSE_PRECEDENCE` | Road waterlogging on ward boundary *(Problem 3)* | **Drainage (`SWD`)** | **Roads (`ROADS`)** | Waterlogging is hydraulically caused by drainage obstruction. Pavement cannot be inspected or resurfaced while submerged. |
| **Priority 3** | `UTILITY_EROSION_PRECEDENCE` | Pressurized water main burst creating road sinkhole | **Water Supply (`MWSSB`)** | **Roads (`ROADS`)** | Pressurized blowout is root cause of cavity. Sluice valve must be isolated and pipe welded before asphalt backfilling. |
| **Priority 4** | `TRANSIT_OBSTRUCTION_PRECEDENCE` | Massive uprooted tree blocking road & median | **Horticulture (`HORT`)** | **Roads (`ROADS`)** | Physical timber trunk must be sectioned with hydraulic chainsaws before median barrier reconstruction can begin. |
| **Priority 5** | `DEBRIS_CLEARANCE_PRECEDENCE` | Dumped commercial garbage choking storm canal | **Solid Waste (`SWM`)** | **Drainage (`SWD`)** | Mechanical grab compactors must scoop surface refuse before drainage divers can enter submerged bed for desilting. |

---

## 🧪 Verification & Testing

Run the automated integration test suite:

```bash
# 1. Verify Gemini status, analysis endpoint, and fallback resilience
python test_gemini_integration.py

# 2. Run the full 8-step Problem 3 simulation suite
python test_problem_3_simulation.py

# 3. Run the 12-case benchmark evaluation suite
python test_dataset_evaluation.py
```
