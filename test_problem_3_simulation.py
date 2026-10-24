"""
Comprehensive Verification Test Client for Problem 3:
Complaints Falling Between Two Departments & Anti-Ping-Pong Deadlock Prevention
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, COMPLAINTS_DB, seed_demo_data

client = TestClient(app)

def run_problem_3_tests():
    print("=" * 80)
    print("PROBLEM 3: COMPLAINTS FALLING BETWEEN TWO DEPARTMENTS")
    print("TESTING WARD BOUNDARY CONFLICTS, DUAL SLAS & ANTI-PING-PONG ESCALATION")
    print("=" * 80)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200
    print("\n[STEP 1] Engine Status: HEALTHY (Version 2.0.0, Problem 3 Compliance Active)")

    # 2. Ingest the Exact Problem 3 Scenario:
    # "A road lies on the boundary between Ward 12 and Ward 13. Heavy rainfall causes severe waterlogging..."
    print("\n[STEP 2] Citizen Reports Severe Waterlogging on Ward 12 / Ward 13 Boundary...")
    complaint_payload = {
        "hazard_type": "water_clogging",
        "description": "Heavy rainfall causes severe waterlogging on GN Chetty Road on the boundary between Ward 12 and Ward 13. Drainage is choked, road flooded 2 feet deep.",
        "ward": "Ward 12 / Ward 13 Boundary Road",
        "is_ward_boundary": True,
        "latitude": 13.0418,
        "longitude": 80.2341,
        "caller_phone": "9840112233"
    }

    ingest_res = client.post("/api/v1/complaints", json=complaint_payload).json()
    cid = ingest_res["complaint_id"]

    print(f"  -> Complaint Registered: {cid}")
    print(f"  -> Conflict Detected:   {ingest_res['is_conflict_detected']} (Type: {ingest_res['conflict_type']})")
    print(f"  -> Primary Assigned:     {ingest_res['primary_department']}")
    print(f"  -> Secondary Partner:    {ingest_res['secondary_department']}")
    print(f"  -> Ownership Rule:       {ingest_res['ownership_rule_applied']}")
    print(f"  -> AI Rationale:         {ingest_res['conflict_resolution_rationale']}")
    print(f"  -> Demonstration SLA:    {ingest_res['demonstration_sla_policy']}")

    assert ingest_res["is_conflict_detected"] is True
    assert "Drainage" in ingest_res["primary_department"]
    assert "Roads" in ingest_res["secondary_department"]
    assert ingest_res["ownership_rule_applied"] == "HYDRAULIC_ROOT_CAUSE_PRECEDENCE"

    # 3. Semi-Automated 1-Click Dispatch:
    print("\n[STEP 3] Administrator Triggers 1-Click Joint Alert Dispatch...")
    dispatch_res = client.post("/api/v1/admin/dispatch-joint-alert", json={
        "complaint_id": cid,
        "admin_id": "CHIEF_DISPATCHER_SHARMA",
        "priority": "CRITICAL",
        "admin_notes": "Emergency dewatering pump dispatch mandated. Roads team on standby."
    }).json()

    assert dispatch_res["status"] == "ALERT_DISPATCHED_SUCCESSFULLY"
    print(f"  -> Alert ID:             {dispatch_res['alert_id']}")
    print(f"  -> Primary Dispatch:     {dispatch_res['primary_department']}")
    print(f"  -> Primary Ack Deadline: {dispatch_res['primary_acknowledgment_deadline']} (5-min policy)")
    print(f"  -> Secondary Dispatch:   {dispatch_res['secondary_department']}")

    # 4. Department A Attempts to Decline ("Road maintenance problem, Roads should do it"):
    print("\n[STEP 4] Department A (Drainage) Attempts to Decline the Issue:")
    print("         \"This is a road-maintenance problem. Department B (Roads) should handle it.\"")
    
    decline_res = client.post("/api/v1/departments/decline", json={
        "complaint_id": cid,
        "declining_department_id": "DEPT_DRAINAGE",
        "reason": "This is a road-maintenance problem. Department of Roads should handle it.",
        "officer_name": "Executive Engineer (Drainage Field)"
    }).json()

    print(f"  -> Intercept Status:     {decline_res['status']}")
    print(f"  -> Action Taken:         {decline_res['action_taken']}")
    print(f"  -> Escalated Authority:  {decline_res['escalated_to']}")
    print(f"  -> In-Charge Officer:    {decline_res['supervisor_in_charge']}")
    print(f"  -> Mandatory Directive:  {decline_res['enforcement_action']}")

    assert decline_res["status"] == "PING_PONG_ROUTING_PREVENTED"
    assert "Supervisor" in decline_res["escalated_to"]

    # 5. Verify Complaint State is Locked (Cannot Ping-Pong):
    c_state = COMPLAINTS_DB[cid]
    assert c_state["status"] == "DISPUTE_ESCALATED_TO_SUPERVISOR"
    assert c_state["is_disputed"] is True
    print("\n[STEP 5] Verified Ticket Status: DISPUTE_ESCALATED_TO_SUPERVISOR (Ping-Pong Loop Blocked)")

    # 6. Test Demonstration SLA Auto-Escalation (Simulate 5-minute Acknowledgment Timeout):
    print("\n[STEP 6] Testing Demonstration SLA Timeout (5 Minutes Without Acknowledgment)...")
    # Simulate an unacknowledged complaint where deadline is in the past
    timeout_cid = f"TIMEOUT-{cid}"
    past_time = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
    c_timeout = dict(c_state)
    c_timeout["complaint_id"] = timeout_cid
    c_timeout["status"] = "ALERT_DISPATCHED"
    c_timeout["dual_slas"]["primary_sla"]["is_acknowledged"] = False
    c_timeout["dual_slas"]["primary_sla"]["acknowledgment_deadline_utc"] = past_time
    COMPLAINTS_DB[timeout_cid] = c_timeout

    escalation_check = client.post("/api/v1/admin/check-sla-escalations").json()
    print(f"  -> Total Complaints Scanned: {escalation_check['total_active_complaints_checked']}")
    print(f"  -> SLA Breaches Escalated:   {escalation_check['sla_breaches_escalated_to_supervisor']}")
    for esc in escalation_check["escalations"]:
        print(f"     Escalated {esc['complaint_id']}: {esc['breaching_department']} breached {esc['acknowledgment_limit_minutes']}m SLA")

    assert escalation_check["sla_breaches_escalated_to_supervisor"] >= 1
    assert COMPLAINTS_DB[timeout_cid]["status"] == "SUPERVISOR_ESCALATED_SLA_BREACH"

    # 7. Test Dedicated 1-Click Judge Demo Simulation:
    print("\n[STEP 7] Testing Dedicated 1-Click Problem 3 Demo Endpoint for Evaluators...")
    demo_run = client.get("/api/v1/demo/problem-3-scenario").json()
    print(f"  -> Demo Title:    {demo_run['challenge_title']}")
    print(f"  -> Scenario:      {demo_run['scenario']}")
    print(f"  -> Steps Executed: {len(demo_run['workflow_steps'])}")
    for s in demo_run["workflow_steps"]:
        print(f"     [Step {s['step']}] {s['action']}")
    print(f"  -> Final Status:  {demo_run['final_status']}")
    assert demo_run["final_status"] == "DISPUTE_ESCALATED_TO_SUPERVISOR"

    # 8. Check Conflict Analytics
    print("\n[STEP 8] Verifying Conflict Analytics & Dispute Audit Trail...")
    analytics = client.get("/api/v1/admin/conflict-analytics").json()
    print(f"  -> Boundary Road Incidents:     {analytics['boundary_road_incidents']}")
    print(f"  -> Department Conflicts Caught: {analytics['departmental_conflicts_identified']}")
    print(f"  -> Ping-Pong Loops Prevented:   {analytics['ping_pong_loops_prevented']}")
    print(f"  -> Supervisor Escalations:      {analytics['supervisor_escalations']}")
    assert analytics["ping_pong_loops_prevented"] >= 1

    print("\n" + "=" * 80)
    print("ALL PROBLEM 3 INTEGRATION TESTS PASSED 100% SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_problem_3_tests()
