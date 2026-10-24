"""
Semi-Automated Municipal Department Assignment & Alert Dispatch Engine (API)
Routes civic hazards to statutory municipal departments in India:
Electricity, Stormwater Drainage, Roads & Infrastructure, Horticulture, and Commissioner Control.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from department_router import (
    STATUTORY_MUNICIPAL_DEPARTMENTS,
    classify_hazard_and_route,
    compute_urgency_risk_score,
    calculate_dynamic_sla,
    detect_ping_pong_deadlock,
    cluster_complaints_by_proximity
)

app = FastAPI(
    title="Semi-Automated Municipal Department Assignment Engine",
    description="Automated Civic Hazard Classification, Department Pre-Routing, 1-Click Alert Dispatch & Boundary Anti-Loop Interceptor",
    version="1.0.0"
)

# Enable CORS for frontend applications (React, Vite, Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# In-Memory Storage for Complaints & Dispatched Alerts
COMPLAINTS_DB: Dict[str, dict] = {}
ALERTS_HISTORY: List[dict] = []

# ---------------------------------------------------------------------------
# REQUEST SCHEMAS
# ---------------------------------------------------------------------------
class ComplaintInput(BaseModel):
    hazard_type: str
    description: str
    latitude: float
    longitude: float
    ward: str = "Central Ward"
    is_ward_boundary: bool = False
    image_url: Optional[str] = None
    caller_phone: Optional[str] = None

class DispatchAlertRequest(BaseModel):
    complaint_id: str
    department_id: str
    admin_id: str = "CHIEF_DISPATCHER_1"
    priority: str = "HIGH"
    admin_notes: Optional[str] = "Field response and immediate inspection mandated."
    override_sla_hours: Optional[int] = None

class ReassignRequest(BaseModel):
    complaint_id: str
    from_department: str
    to_department: str
    reassigned_by: str
    reason: str

# ---------------------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Semi-Automated Municipal Department Assignment Engine",
        "version": "1.0.0",
        "statutory_departments_count": len(STATUTORY_MUNICIPAL_DEPARTMENTS),
        "total_active_complaints": len(COMPLAINTS_DB)
    }

@app.post("/api/v1/complaints")
async def register_civic_complaint(req: ComplaintInput):
    """
    Ingests a civic complaint, automatically identifies the problem type,
    pre-selects the concerned municipal department, and calculates urgency risk score.
    """
    complaint_id = f"CMP-{uuid.uuid4().hex[:6].upper()}"
    now_str = datetime.now(timezone.utc).isoformat()

    # Automated problem classification & department routing
    routing = classify_hazard_and_route(req.hazard_type, req.description)
    risk = compute_urgency_risk_score(req.hazard_type, req.description)

    complaint = {
        "complaint_id": complaint_id,
        "hazard_type": req.hazard_type,
        "description": req.description,
        "coordinates": {"latitude": req.latitude, "longitude": req.longitude},
        "coarse_coordinates": {"latitude": round(req.latitude, 3), "longitude": round(req.longitude, 3)},
        "ward": req.ward,
        "is_ward_boundary": req.is_ward_boundary,
        "image_url": req.image_url,
        "caller_phone": req.caller_phone,
        "detected_problem": routing["detected_problem"],
        "pre_selected_department_id": routing["recommended_department_id"],
        "pre_selected_department_name": routing["recommended_department_name"],
        "department_code": routing["department_code"],
        "routing_confidence": routing["confidence"],
        "risk_score": risk["risk_score"],
        "suggested_priority": risk["priority"],
        "status": "PENDING_ADMIN_DISPATCH",
        "assigned_department": None,
        "alert_dispatched": False,
        "alert_payload": None,
        "sla": None,
        "reassignment_hops": [],
        "created_at": now_str,
        "history": [{"action": "INGESTED", "timestamp": now_str}]
    }

    COMPLAINTS_DB[complaint_id] = complaint

    return {
        "status": "REGISTERED",
        "complaint_id": complaint_id,
        "detected_problem": routing["detected_problem"],
        "pre_selected_department": routing["recommended_department_name"],
        "department_code": routing["department_code"],
        "urgency_score": risk["risk_score"],
        "priority": risk["priority"],
        "action_required": "Review pre-selected department and trigger 1-click dispatch"
    }

@app.get("/api/v1/admin/inbox")
async def get_admin_dispatch_inbox():
    """
    Administrator Inbox: Shows complaints waiting for semi-automated Alert dispatch,
    sorted with highest-risk emergencies at the top.
    """
    pending = [c for c in COMPLAINTS_DB.values() if c.get("status") == "PENDING_ADMIN_DISPATCH"]
    pending.sort(key=lambda x: x.get("risk_score", 50), reverse=True)
    return {
        "total_pending_dispatches": len(pending),
        "complaints": pending
    }

@app.get("/api/v1/admin/departments")
async def get_statutory_departments():
    """
    Returns list of all statutory municipal departments with in-charge officers,
    alert channels, and active workload counts.
    """
    depts = []
    for d_id, d in STATUTORY_MUNICIPAL_DEPARTMENTS.items():
        active = sum(1 for c in COMPLAINTS_DB.values() if c.get("assigned_department") == d_id and c.get("status") in ["ALERT_DISPATCHED", "IN_PROGRESS"])
        depts.append({
            "department_id": d["id"],
            "department_name": d["name"],
            "code": d["code"],
            "in_charge": d["in_charge"],
            "handles": d["handles"],
            "alert_channel": d["alert_channel"],
            "active_workload": active,
            "sla_policy_hours": d["sla_hours"]
        })
    return {"departments": depts}

@app.post("/api/v1/admin/dispatch-alert")
async def dispatch_alert_to_department(req: DispatchAlertRequest):
    """
    SEMI-AUTOMATED 1-CLICK DISPATCH:
    Administrator confirms or modifies department, dynamic SLA clock starts,
    and a rich operational payload is transmitted to the concerned department.
    """
    if req.complaint_id not in COMPLAINTS_DB:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if req.department_id not in STATUTORY_MUNICIPAL_DEPARTMENTS:
        raise HTTPException(status_code=400, detail="Invalid Department ID")

    complaint = COMPLAINTS_DB[req.complaint_id]
    dept = STATUTORY_MUNICIPAL_DEPARTMENTS[req.department_id]
    sla = calculate_dynamic_sla(req.department_id, req.priority, req.override_sla_hours)
    now_str = datetime.now(timezone.utc).isoformat()
    alert_id = f"ALT-{uuid.uuid4().hex[:6].upper()}"

    # Complete operational alert payload delivered to department
    alert_payload = {
        "alert_id": alert_id,
        "complaint_id": req.complaint_id,
        "dispatched_at_utc": now_str,
        "dispatched_by_admin": req.admin_id,
        "concerned_department": {
            "department_id": dept["id"],
            "department_name": dept["name"],
            "department_code": dept["code"],
            "in_charge_officer": dept["in_charge"],
            "alert_channel": dept["alert_channel"]
        },
        "incident_details": {
            "detected_problem": complaint["detected_problem"],
            "priority_level": req.priority,
            "risk_score": complaint["risk_score"],
            "ward": complaint["ward"],
            "is_ward_boundary": complaint["is_ward_boundary"],
            "exact_gps_coordinates": complaint["coordinates"],
            "caller_description": complaint["description"],
            "admin_dispatch_notes": req.admin_notes,
            "image_evidence_url": complaint.get("image_url")
        },
        "sla_enforcement": {
            "allowed_hours_limit": sla["allowed_hours_limit"],
            "sla_target_deadline_utc": sla["sla_target_deadline_utc"],
            "probabilistic_eta_range": sla["probabilistic_eta_range"]
        }
    }

    # Update complaint state
    complaint["assigned_department"] = req.department_id
    complaint["assigned_department_name"] = dept["name"]
    complaint["department_code"] = dept["code"]
    complaint["status"] = "ALERT_DISPATCHED"
    complaint["alert_dispatched"] = True
    complaint["alert_payload"] = alert_payload
    complaint["sla"] = sla
    complaint["history"].append({
        "action": "ALERT_DISPATCHED",
        "admin_id": req.admin_id,
        "department": dept["name"],
        "priority": req.priority,
        "timestamp": now_str
    })

    ALERTS_HISTORY.append(alert_payload)

    return {
        "status": "ALERT_DISPATCHED_SUCCESSFULLY",
        "complaint_id": req.complaint_id,
        "alert": alert_payload
    }

@app.get("/api/v1/admin/dispatched-alerts")
async def get_dispatched_alerts():
    """
    Returns list of all active dispatches currently with field repair crews,
    including department, assigned priority, and SLA target deadline.
    """
    return {
        "total_active_alerts": len(ALERTS_HISTORY),
        "dispatches": ALERTS_HISTORY
    }

@app.get("/api/v1/admin/clusters")
async def get_incident_clusters(max_distance_meters: float = Query(80.0, ge=10.0, le=500.0)):
    """
    Spatio-Temporal Incident Clustering:
    Groups citizen complaints within 80 meters belonging to the same department.
    Prevents dispatching duplicate crews to the same incident during monsoon storms.
    """
    all_complaints = list(COMPLAINTS_DB.values())
    clusters = cluster_complaints_by_proximity(all_complaints, max_distance_meters=max_distance_meters)
    return {
        "total_clusters": len(clusters),
        "total_complaints_analyzed": len(all_complaints),
        "clusters": clusters
    }

@app.get("/api/v1/public/complaints")
async def list_public_complaints():
    """Returns list of public reports for citizen map/feed (coarse coordinates, status)."""
    feed = []
    for c in COMPLAINTS_DB.values():
        feed.append({
            "complaint_id": c["complaint_id"],
            "detected_problem": c["detected_problem"],
            "ward": c["ward"],
            "status": c["status"],
            "assigned_department": c.get("assigned_department_name", "Municipal Review In-Progress"),
            "approximate_location": c.get("coarse_coordinates") or {"latitude": round(c["coordinates"]["latitude"], 3), "longitude": round(c["coordinates"]["longitude"], 3)},
            "probabilistic_eta": c["sla"]["probabilistic_eta_range"] if c.get("sla") else "Pending Dispatch",
            "created_at": c["created_at"]
        })
    return {"total": len(feed), "complaints": feed}

@app.post("/api/v1/admin/reassign")
async def reassign_with_anti_loop(req: ReassignRequest):
    """
    Reassigns ticket between departments.
    Intercepts jurisdictional boundary disputes (Department A -> Dept B -> Dept A)
    and auto-escalates directly to the Municipal Commissioner's Emergency Cell.
    """
    if req.complaint_id not in COMPLAINTS_DB:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint = COMPLAINTS_DB[req.complaint_id]
    now_str = datetime.now(timezone.utc).isoformat()
    hops = complaint.get("reassignment_hops", [])

    hops.append({
        "from": req.from_department,
        "to": req.to_department,
        "by": req.reassigned_by,
        "reason": req.reason,
        "timestamp": now_str
    })
    complaint["reassignment_hops"] = hops

    # PING-PONG DEADLOCK CHECK
    if detect_ping_pong_deadlock(hops):
        deadlock_dept_id = "DEPT_EMERGENCY_CELL"
        commissioner_dept = STATUTORY_MUNICIPAL_DEPARTMENTS[deadlock_dept_id]
        emergency_sla = calculate_dynamic_sla(deadlock_dept_id, "CRITICAL", custom_hours=1)

        complaint["assigned_department"] = deadlock_dept_id
        complaint["assigned_department_name"] = commissioner_dept["name"]
        complaint["department_code"] = commissioner_dept["code"]
        complaint["status"] = "DEADLOCK_ESCALATED"
        complaint["is_deadlocked"] = True
        complaint["sla"] = emergency_sla
        complaint["history"].append({
            "action": "PING_PONG_LOOP_INTERCEPTED",
            "alert": "Jurisdictional boundary dispute detected. Both departments rejected ticket.",
            "escalated_to": commissioner_dept["name"],
            "timestamp": now_str
        })

        return {
            "status": "DEADLOCK_TRIGGERED",
            "message": "Ping-pong loop intercepted! Boundary dispute escalated to Municipal Commissioner's Control Room.",
            "escalated_owner": commissioner_dept["name"],
            "department_code": commissioner_dept["code"],
            "emergency_sla": emergency_sla
        }

    # Standard reassignment
    new_dept = STATUTORY_MUNICIPAL_DEPARTMENTS[req.to_department]
    complaint["assigned_department"] = req.to_department
    complaint["assigned_department_name"] = new_dept["name"]
    complaint["department_code"] = new_dept["code"]
    complaint["status"] = "ALERT_REASSIGNED"
    new_sla = calculate_dynamic_sla(req.to_department, complaint.get("suggested_priority", "HIGH"))
    complaint["sla"] = new_sla
    complaint["history"].append({
        "action": "REASSIGNED",
        "from": req.from_department,
        "to": req.to_department,
        "reason": req.reason,
        "timestamp": now_str
    })

    return {
        "status": "REASSIGNED_SUCCESSFULLY",
        "new_department": new_dept["name"],
        "sla": new_sla
    }

@app.get("/api/v1/admin/dashboard-stats")
async def get_dashboard_stats():
    """Returns top-level KPI metrics for the Municipal Administrator Console."""
    total = len(COMPLAINTS_DB)
    pending = sum(1 for c in COMPLAINTS_DB.values() if c.get("status") == "PENDING_ADMIN_DISPATCH")
    dispatched = sum(1 for c in COMPLAINTS_DB.values() if c.get("status") == "ALERT_DISPATCHED")
    deadlocked = sum(1 for c in COMPLAINTS_DB.values() if c.get("status") == "DEADLOCK_ESCALATED")
    critical = sum(1 for c in COMPLAINTS_DB.values() if c.get("risk_score", 0) >= 90)

    dept_counts = {k: 0 for k in STATUTORY_MUNICIPAL_DEPARTMENTS}
    for c in COMPLAINTS_DB.values():
        dept = c.get("assigned_department") or c.get("pre_selected_department_id")
        if dept in dept_counts:
            dept_counts[dept] += 1

    return {
        "total_complaints": total,
        "pending_dispatches": pending,
        "alerts_dispatched": dispatched,
        "deadlock_escalations": deadlocked,
        "critical_priority_hazards": critical,
        "department_distribution": dept_counts
    }

@app.get("/api/v1/public/complaints/{complaint_id}")
async def get_public_tracking(complaint_id: str):
    """Citizen tracking view."""
    if complaint_id not in COMPLAINTS_DB:
        raise HTTPException(status_code=404, detail="Complaint not found")
    c = COMPLAINTS_DB[complaint_id]
    return {
        "complaint_id": c["complaint_id"],
        "detected_problem": c["detected_problem"],
        "ward": c["ward"],
        "status": c["status"],
        "assigned_department": c.get("assigned_department_name", "Municipal Review In-Progress"),
        "probabilistic_eta": c["sla"]["probabilistic_eta_range"] if c.get("sla") else "Pending Dispatch",
        "created_at": c["created_at"]
    }

@app.post("/api/v1/admin/seed-demo-data")
async def seed_demo_data(force: bool = False):
    """Seeds 4 realistic municipal complaints into the database."""
    if len(COMPLAINTS_DB) > 0 and not force:
        return {"status": "ALREADY_POPULATED", "total_complaints": len(COMPLAINTS_DB)}

    COMPLAINTS_DB.clear()
    seeds = [
        {
            "hazard_type": "electricity_hazard",
            "description": "High voltage live wire snapped and sparking in standing rainwater near primary school. Extreme shock danger!",
            "lat": 13.0827, "lng": 80.2707, "ward": "Ward 77 - Egmore"
        },
        {
            "hazard_type": "water_clogging",
            "description": "Severe monsoon waterlogging at arterial road junction. Stormwater drain blocked with plastic, knee-deep flood.",
            "lat": 13.0482, "lng": 80.2214, "ward": "Ward 112 - T. Nagar"
        },
        {
            "hazard_type": "tree_debris",
            "description": "Massive uprooted banyan tree trunk blocking north bus lane after storm. Heavy tree debris on tarmac.",
            "lat": 13.0331, "lng": 80.2452, "ward": "Ward 140 - Alwarpet"
        },
        {
            "hazard_type": "road_potholes",
            "description": "Dangerous deep asphalt crater pothole causing vehicle tire damage and skidding on flyover descent ramp.",
            "lat": 13.0603, "lng": 80.2501, "ward": "Ward 95 - Anna Salai"
        }
    ]

    for s in seeds:
        routing = classify_hazard_and_route(s["hazard_type"], s["description"])
        risk = compute_urgency_risk_score(s["hazard_type"], s["description"])
        cid = f"CMP-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now(timezone.utc).isoformat()

        COMPLAINTS_DB[cid] = {
            "complaint_id": cid,
            "hazard_type": s["hazard_type"],
            "description": s["description"],
            "coordinates": {"latitude": s["lat"], "longitude": s["lng"]},
            "coarse_coordinates": {"latitude": round(s["lat"], 3), "longitude": round(s["lng"], 3)},
            "ward": s["ward"],
            "is_ward_boundary": False,
            "detected_problem": routing["detected_problem"],
            "pre_selected_department_id": routing["recommended_department_id"],
            "pre_selected_department_name": routing["recommended_department_name"],
            "department_code": routing["department_code"],
            "routing_confidence": routing["confidence"],
            "risk_score": risk["risk_score"],
            "suggested_priority": risk["priority"],
            "status": "PENDING_ADMIN_DISPATCH",
            "assigned_department": None,
            "alert_dispatched": False,
            "alert_payload": None,
            "sla": None,
            "reassignment_hops": [],
            "created_at": now,
            "history": [{"action": "SEEDED_FOR_DEMO", "timestamp": now}]
        }

    return {"status": "SUCCESS", "message": "Seeded 4 realistic municipal complaints", "total": len(COMPLAINTS_DB)}

@app.on_event("startup")
async def startup_event():
    await seed_demo_data(force=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
