"""
Verification Test Client for Semi-Automated Municipal Department Assignment Engine
Tests automated hazard classification, pre-routing, 1-click alert dispatch, and anti-loop interceptor.
"""

import sys
from fastapi.testclient import TestClient
from app import app, COMPLAINTS_DB, seed_demo_data

client = TestClient(app)

def run_tests():
    print("=" * 75)
    print("TESTING SEMI-AUTOMATED MUNICIPAL DEPARTMENT ASSIGNMENT & ALERT DISPATCH")
    print("=" * 75)

    # 1. Verify Statutory Departments
    print("\n--- 1. Fetching Statutory Municipal Departments ---")
    resp = client.get("/api/v1/admin/departments")
    assert resp.status_code == 200
    depts = resp.json()["departments"]
    print(f"Total Configured Departments: {len(depts)}")
    for d in depts:
        print(f"  [{d['code']}] {d['department_name']} -> {d['in_charge']}")

    # 2. Ingest New Live Wire Hazard
    print("\n--- 2. Ingesting Live Wire Emergency Hazard ---")
    wire_res = client.post("/api/v1/complaints", json={
        "hazard_type": "electricity_hazard",
        "description": "High voltage snapped electric line sparking in puddle near school bus stop! Urgent risk.",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "ward": "Ward 77 - Egmore",
        "caller_phone": "9840112233"
    }).json()

    print(f"Complaint ID:     {wire_res['complaint_id']}")
    print(f"Detected Problem: {wire_res['detected_problem']}")
    print(f"Pre-Selected:     {wire_res['pre_selected_department']} [{wire_res['department_code']}]")
    print(f"Urgency Score:    {wire_res['urgency_score']}/100 (Priority: {wire_res['priority']})")
    assert wire_res["department_code"] == "ELEC"
    assert wire_res["urgency_score"] == 98
    cid = wire_res["complaint_id"]

    # 3. Check Admin Inbox
    print("\n--- 3. Verifying Admin Dispatch Queue ---")
    inbox = client.get("/api/v1/admin/inbox").json()
    print(f"Pending Dispatches in Queue: {inbox['total_pending_dispatches']}")
    top = inbox["complaints"][0]
    print(f"Top Priority in Queue: {top['complaint_id']} (Score: {top['risk_score']}) -> {top['pre_selected_department_name']}")

    # 4. Administrator 1-Click Alert Dispatch
    print("\n--- 4. Administrator 1-Click Alert Dispatch to Electricity Department ---")
    alert_resp = client.post("/api/v1/admin/dispatch-alert", json={
        "complaint_id": cid,
        "department_id": "DEPT_ELECTRICITY",
        "admin_id": "SENIOR_DISPATCHER_RAO",
        "priority": "CRITICAL",
        "admin_notes": "Immediate lineman crew dispatch and power feeder trip mandated."
    }).json()

    assert alert_resp["status"] == "ALERT_DISPATCHED_SUCCESSFULLY"
    alert = alert_resp["alert"]
    print(f"Alert ID:            {alert['alert_id']}")
    print(f"Dispatched To:       {alert['concerned_department']['department_name']} ({alert['concerned_department']['department_code']})")
    print(f"Emergency Channel:   {alert['concerned_department']['alert_channel']}")
    print(f"SLA Target Window:   {alert['sla_enforcement']['probabilistic_eta_range']}")

    # 5. Test Ping-Pong Boundary Loop Deadlock Breaker
    print("\n--- 5. Testing Boundary Dispute Ping-Pong Deadlock Breaker ---")
    # Hop 1: Drainage rejects to Roads
    client.post("/api/v1/admin/reassign", json={
        "complaint_id": cid,
        "from_department": "DEPT_DRAINAGE",
        "to_department": "DEPT_ROADS",
        "reassigned_by": "DRAINAGE_OFFICER",
        "reason": "Water clogging caused by uneven road surface."
    })

    # Hop 2: Roads rejects back to Drainage (Loop Detected!)
    deadlock_res = client.post("/api/v1/admin/reassign", json={
        "complaint_id": cid,
        "from_department": "DEPT_ROADS",
        "to_department": "DEPT_DRAINAGE",
        "reassigned_by": "ROADS_OFFICER",
        "reason": "Road is clear, storm drain is silted."
    }).json()

    print(f"Loop Status:         {deadlock_res['status']}")
    print(f"Message:             {deadlock_res['message']}")
    print(f"Auto-Escalated To:   {deadlock_res['escalated_owner']} [{deadlock_res['department_code']}]")
    print(f"Emergency Window:    {deadlock_res['emergency_sla']['probabilistic_eta_range']}")
    assert deadlock_res["status"] == "DEADLOCK_TRIGGERED"

    # 6. Verify Dashboard Stats
    print("\n--- 6. Verifying Dashboard KPI Metrics ---")
    stats = client.get("/api/v1/admin/dashboard-stats").json()
    print(f"Total Complaints:    {stats['total_complaints']}")
    print(f"Deadlock Escalations:{stats['deadlock_escalations']}")
    print(f"Critical Hazards:    {stats['critical_priority_hazards']}")

    print("\n" + "=" * 75)
    print("ALL TESTS PASSED! MUNICIPAL ASSIGNMENT ENGINE 100% OPERATIONAL")
    print("=" * 75)

if __name__ == "__main__":
    run_tests()
