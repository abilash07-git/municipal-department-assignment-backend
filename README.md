# Semi-Automated Municipal Department Assignment & Alert Dispatch Engine

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated, intelligent backend routing and alert dispatch microservice designed for **Municipal Corporations in India**.

It automatically ingests civic complaints, classifies the civic hazard, pre-selects the strictly concerned municipal department, computes dynamic urgency risk scores and SLA clocks, and empowers the municipal administrator to trigger **semi-automated rich alert dispatches** with a single click.

---

## 🏛️ Statutory Municipal Departments Configured

The engine maps all incoming civic issues directly to authorized statutory municipal authorities:

| # | Code | Department Name | In-Charge Officer | Official Emergency Alert Channel | SLA Clock (Critical / High) |
|---|---|---|---|---|---|
| **1** | **`ELEC`** | **Electricity & Street Lighting Department** | Superintending Engineer (Power Distribution & Lighting) | `electricity-emergency@municipal.gov.in` \| VHF Ch-3 \| Hotline **1912** | **1 hr** / **3 hrs** |
| **2** | **`SWD`** | **Stormwater Drainage & Flood Mitigation** | Executive Engineer (Stormwater Drainage & Flood Control) | `drainage-emergency@municipal.gov.in` \| VHF Ch-4 \| Hotline **1077** | **2 hrs** / **4 hrs** |
| **3** | **`ROADS`** | **Roads & Infrastructure Department** | Executive Engineer (Road Maintenance & Pothole Repair) | `roads-repair@municipal.gov.in` \| VHF Ch-2 \| Helpline **1916** | **3 hrs** / **6 hrs** |
| **4** | **`HORT`** | **Horticulture & Tree Authority** | Superintendent of Gardens & Tree Officer | `trees-emergency@municipal.gov.in` \| VHF Ch-5 \| Helpline **1099** | **2 hrs** / **5 hrs** |
| **5** | **`COMM-CTRL`**| **Municipal Commissioner's Emergency Cell** | Additional Municipal Commissioner (Disaster Operations) | `commissioner-control@municipal.gov.in` \| Control Room **101** | **1 hr** (Emergency Escalation) |

---

## ⚡ Core Engine Features

1. **Automated Problem Classification & Pre-Routing**:
   * Analyzes incoming complaint text and keywords.
   * Auto-detects problem type:
     * *Live Wire / Electrical Hazard & Street Lighting* $\rightarrow$ Pre-selects **`DEPT_ELECTRICITY`**
     * *Water Clogging & Drainage Issue* $\rightarrow$ Pre-selects **`DEPT_DRAINAGE`**
     * *Road Potholes & Infrastructure Damage* $\rightarrow$ Pre-selects **`DEPT_ROADS`**
     * *Tree Debris & Transit Obstruction* $\rightarrow$ Pre-selects **`DEPT_HORTICULTURE`**
2. **Urgency Risk Scoring (0–100) & Priority Tiers**:
   * Evaluates life-safety risks (e.g. snapped high-voltage lines score **98/100, CRITICAL**; open manholes score **94/100, CRITICAL**).
3. **Semi-Automated 1-Click Alert Dispatch**:
   * The administrator reviews the incoming queue with the recommended department pre-filled.
   * Clicking **"Send Alert"** triggers a rich, structured operational payload to the department's emergency channels.
4. **Dynamic Probabilistic SLA Clocks**:
   * Computes dynamic resolution deadlines with probabilistic weather ranges (e.g. *"1 to 3 hours subject to monsoon weather severity"*).
5. **Anti-Ping-Pong Boundary Deadlock Interceptor**:
   * If two departments reject a complaint back and forth on a ward boundary road (Dept A $\rightarrow$ Dept B $\rightarrow$ Dept A), the engine intercepts the loop and **auto-escalates to the Municipal Commissioner's Control Room** with a mandatory 1-hour resolution order.
6. **Zero-Setup Startup Auto-Seeding**:
   * Automatically pre-seeds 4 realistic civic complaints on boot so frontends immediately have active cards to display.

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend Server
```bash
python app.py
```
* **Server Address:** `http://localhost:8000`
* **Interactive Swagger API Docs:** `http://localhost:8000/docs`

### Step 3: Run Verification Test
```bash
python test_client.py
```

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/api/v1/complaints` | Ingests civic complaint, auto-classifies problem & pre-selects department |
| `GET` | `/api/v1/admin/inbox` | Administrator Dispatch Queue sorted by descending urgency risk |
| `GET` | `/api/v1/admin/departments` | Returns list of statutory municipal departments with in-charge contacts |
| `POST` | `/api/v1/admin/dispatch-alert` | **1-Click Dispatch:** Fires rich alert payload to concerned department |
| `GET` | `/api/v1/admin/dispatched-alerts` | Returns list of all active field dispatches with live SLA clocks |
| `GET` | `/api/v1/admin/clusters` | **Spatio-Temporal Clustering:** Groups nearby overlapping reports (<= 80m) |
| `POST` | `/api/v1/admin/reassign` | Reassigns ticket & intercepts Ping-Pong reassignment loops |
| `GET` | `/api/v1/admin/dashboard-stats` | KPI summary cards: total tickets, pending, dispatched, deadlocks |
| `GET` | `/api/v1/public/complaints` | Public citizen feed/map view with 100m coarse coordinates |
| `GET` | `/api/v1/public/complaints/{id}`| Citizen tracking view with status and probabilistic ETA range |
| `POST` | `/api/v1/admin/seed-demo-data` | Resets/re-seeds the 4 demo municipal complaints anytime |

---

## 📦 Full Operational Alert Payload Delivered to Department

When the administrator triggers `POST /api/v1/admin/dispatch-alert`, the concerned department receives this complete payload:

```json
{
  "alert_id": "ALT-6363A7",
  "complaint_id": "CMP-BCBDFD",
  "dispatched_at_utc": "2026-10-25T02:42:55.123456+00:00",
  "dispatched_by_admin": "SENIOR_DISPATCHER_RAO",
  "concerned_department": {
    "department_id": "DEPT_ELECTRICITY",
    "department_name": "Electricity & Street Lighting Department",
    "department_code": "ELEC",
    "in_charge_officer": "Superintending Engineer (Power Distribution & Street Lighting)",
    "alert_channel": "electricity-emergency@municipal.gov.in | VHF Ch-3 | Emergency Helpline 1912"
  },
  "incident_details": {
    "detected_problem": "Live Wire / Electrical Hazard & Street Lighting",
    "priority_level": "CRITICAL",
    "risk_score": 98,
    "ward": "Ward 77 - Egmore",
    "is_ward_boundary": false,
    "exact_gps_coordinates": {
      "latitude": 13.0827,
      "longitude": 80.2707
    },
    "caller_description": "High voltage snapped electric line sparking in puddle near school bus stop! Urgent risk.",
    "admin_dispatch_notes": "Immediate lineman crew dispatch and power feeder trip mandated."
  },
  "sla_enforcement": {
    "allowed_hours_limit": 1,
    "sla_target_deadline_utc": "2026-10-25T03:42:55.123456+00:00",
    "probabilistic_eta_range": "1 to 1 hours (subject to monsoon weather severity)"
  }
}
```

---

## 💻 Ready-to-Use Frontend Integration Component (React + Tailwind CSS)

You can copy and drop this React component directly into your frontend:

```tsx
import React, { useState, useEffect } from 'react';

export const MunicipalDispatchConsole = () => {
  const [complaints, setComplaints] = useState([]);
  const [selectedDept, setSelectedDept] = useState({});
  const [stats, setStats] = useState(null);

  const loadData = () => {
    fetch('http://localhost:8000/api/v1/admin/dashboard-stats')
      .then(r => r.json()).then(setStats);

    fetch('http://localhost:8000/api/v1/admin/inbox')
      .then(r => r.json())
      .then(data => {
        setComplaints(data.complaints || []);
        const map = {};
        (data.complaints || []).forEach(c => {
          map[c.complaint_id] = c.pre_selected_department_id;
        });
        setSelectedDept(map);
      });
  };

  useEffect(() => { loadData(); }, []);

  const handleSendAlert = async (c) => {
    const res = await fetch('http://localhost:8000/api/v1/admin/dispatch-alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        complaint_id: c.complaint_id,
        department_id: selectedDept[c.complaint_id],
        admin_id: "CHIEF_DISPATCHER",
        priority: c.suggested_priority,
        admin_notes: "Emergency field action mandated by municipal administrator."
      })
    });
    const data = await res.json();
    alert(`Alert Dispatched to: ${data.alert.concerned_department.department_name}`);
    loadData();
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Municipal Alert Dispatch Console</h1>
        {stats && (
          <div className="flex gap-2">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-xs font-bold">Total: {stats.total_complaints}</span>
            <span className="bg-amber-100 text-amber-800 px-3 py-1 rounded text-xs font-bold">Pending: {stats.pending_dispatches}</span>
            <span className="bg-red-100 text-red-800 px-3 py-1 rounded text-xs font-bold">Critical: {stats.critical_priority_hazards}</span>
          </div>
        )}
      </div>

      <div className="space-y-4">
        {complaints.map(c => (
          <div key={c.complaint_id} className="p-5 border rounded-lg bg-white shadow-sm flex flex-col gap-3">
            <div className="flex justify-between items-start">
              <div>
                <span className={`px-2 py-0.5 text-xs font-bold rounded ${
                  c.risk_score >= 90 ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'
                }`}>
                  Score: {c.risk_score}/100 ({c.suggested_priority})
                </span>
                <h3 className="text-lg font-bold text-gray-900 mt-1">{c.detected_problem}</h3>
              </div>
              <span className="text-xs font-mono text-gray-500">{c.complaint_id} • {c.ward}</span>
            </div>

            <p className="text-sm text-gray-600">{c.description}</p>

            <div className="flex items-center gap-3 pt-2 border-t">
              <label className="text-xs font-semibold text-gray-500">Assign Department:</label>
              <select
                value={selectedDept[c.complaint_id]}
                onChange={e => setSelectedDept({...selectedDept, [c.complaint_id]: e.target.value})}
                className="text-sm border rounded px-3 py-1.5 font-medium bg-gray-50"
              >
                <option value="DEPT_ELECTRICITY">Electricity & Street Lighting (ELEC)</option>
                <option value="DEPT_DRAINAGE">Stormwater Drainage (SWD)</option>
                <option value="DEPT_ROADS">Roads & Infrastructure (ROADS)</option>
                <option value="DEPT_HORTICULTURE">Horticulture & Tree Authority (HORT)</option>
              </select>

              <button
                onClick={() => handleSendAlert(c)}
                className="ml-auto bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-4 py-1.5 rounded shadow transition"
              >
                Send Alert with Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```
