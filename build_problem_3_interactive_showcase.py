"""
Builder for Problem 3 Interactive Workflow Showcase HTML Widget
Renders rich interactive HTML widget for demonstrating the 5 real-world dataset cases,
dynamic dual SLA countdown timers, interactive decline simulations, and supervisor escalations.
"""

import os
import json

ARTIFACT_DIR = r"C:\Users\Lenovo\.gemini\antigravity\brain\82af6ceb-bb74-4b65-8996-16630260df13"
HTML_PATH = os.path.join(ARTIFACT_DIR, "problem_3_interactive_showcase.html")

SHOWCASE_DATA = [
    {
        "id": "case1",
        "tab_label": "Case 1: Waterlogging (Drainage vs Roads)",
        "badge": "BENCHMARK PROBLEM 3 SCENARIO",
        "title": "Ward 12 & 13 Boundary Road Waterlogging",
        "location": "GN Chetty Arterial Boundary Road (Ward 12 / Ward 13 Border)",
        "coords": "13.0418° N, 80.2341° E",
        "input_img": "input_raw_case1_waterlogging.jpg",
        "workflow_card": "workflow_case_1_waterlogging_road.jpg",
        "hazard_type": "WATERLOGGING_ROAD",
        "description": "Severe 2.5 feet standing waterlogging on GN Chetty boundary road following 85mm rainfall. Multiple cars and auto-rickshaws stalled in water. Storm drain inlet completely submerged.",
        "conflict_type": "BOUNDARY_ROAD_DUAL_INFRASTRUCTURE",
        "primary_dept": "Stormwater Drainage & Flood Mitigation (SWD)",
        "primary_role": "LEAD_RESPONDER (Deploy high-capacity suction pumps & clear submerged culvert)",
        "secondary_dept": "Roads & Infrastructure Department (ROADS)",
        "secondary_role": "JOINT_SUPPORT_COORDINATOR (Inspect pavement & patch potholes once water recedes)",
        "rule_applied": "HYDRAULIC_ROOT_CAUSE_PRECEDENCE",
        "rule_rationale": "Waterlogging on road is hydraulically caused by drainage blockage. Dewatering and drain clearance is prerequisite before road damage inspection or asphalt resurfacing.",
        "primary_sla_ack": "5 Minutes (Critical Safety Demo Policy)",
        "primary_sla_res": "2 Hours (Full Dewatering Complete)",
        "secondary_sla_ack": "15 Minutes",
        "secondary_sla_res": "4 Hours (Post-Dewatering Inspection)",
        "decline_simulation": {
            "dept": "Stormwater Drainage Dept (SWD)",
            "officer": "Er. K. Ramanathan (Executive Engineer)",
            "quote": "This is a road-maintenance problem. Road surface has depressions and poor asphalt camber. Department B (Roads) should handle it.",
            "intercept_msg": "Ping-pong bounce to Roads Department BLOCKED. Escalated to Zonal Joint Municipal Commissioner.",
            "directive_id": "JD-2026-904"
        }
    },
    {
        "id": "case2",
        "tab_label": "Case 2: Live Power Line (Electricity vs Horticulture)",
        "badge": "LIFE-SAFETY OVERRIDE",
        "title": "Snapped High-Voltage Wire in Tree Foliage",
        "location": "Gandhi Irwin Boundary Canal Road (Ward 77 / Ward 78 Border)",
        "coords": "13.0827° N, 80.2707° E",
        "input_img": "input_raw_case2_live_wire.jpg",
        "workflow_card": "workflow_case_2_live_wire_tree.jpg",
        "hazard_type": "LIVE_WIRE_TREE",
        "description": "High-voltage 440V distribution wire snapped and sparking actively in tree foliage directly above public pedestrian sidewalk and carriageway.",
        "conflict_type": "LIVE_POWER_AND_TREE_ENTANGLEMENT",
        "primary_dept": "Electricity & Street Lighting Department (ELEC)",
        "primary_role": "LEAD_RESPONDER (De-energize substation feeder & ground live conductor)",
        "secondary_dept": "Horticulture & Tree Authority (HORT)",
        "secondary_role": "JOINT_SUPPORT_COORDINATOR (Saw tree limbs once certified electrically isolated)",
        "rule_applied": "LIFE_SAFETY_ISOLATION_PRECEDENCE",
        "rule_rationale": "Imminent electrocution hazard takes absolute life-safety priority. Substation feeder must be de-energized and certified safe by Electricity Department before Horticulture team can saw tree limbs.",
        "primary_sla_ack": "5 Minutes (Critical Safety Demo Policy)",
        "primary_sla_res": "1 Hour (Grid Isolation & Grounding)",
        "secondary_sla_ack": "15 Minutes",
        "secondary_sla_res": "2 Hours (Tree Limb Clearance)",
        "decline_simulation": {
            "dept": "Electricity Department (ELEC)",
            "officer": "Er. S. Murugan (Divisional Engineer)",
            "quote": "Heavy overgrown tree branches caused the wire snap. Horticulture Department must prune and clear the tree limbs before we can restore lines.",
            "intercept_msg": "Unilateral decline rejected. High-voltage isolation cannot be delegated. Escalated to Municipal Commissioner.",
            "directive_id": "JD-2026-905"
        }
    },
    {
        "id": "case3",
        "tab_label": "Case 3: Pipe Burst Crater (Water Supply vs Roads)",
        "badge": "UTILITY EROSION PRECEDENCE",
        "title": "Underground Water Main Burst & Road Crater",
        "location": "Luz Church Boundary Avenue (Ward 112 / Ward 113 Border)",
        "coords": "13.0331° N, 80.2612° E",
        "input_img": "input_raw_case3_pipe_burst.jpg",
        "workflow_card": "workflow_case_3_pipe_burst_road.jpg",
        "hazard_type": "PIPE_BURST_ROAD",
        "description": "Active pressurized drinking water pipeline burst causing 4-foot deep subterranean crater and road cave-in on arterial boundary road.",
        "conflict_type": "UNDERGROUND_PIPE_BURST_AND_ROAD_CAVE_IN",
        "primary_dept": "Metro Water Supply & Sewerage Board (MWSSB)",
        "primary_role": "LEAD_RESPONDER (Isolate valve sluice & weld/replace broken main)",
        "secondary_dept": "Roads & Infrastructure Department (ROADS)",
        "secondary_role": "JOINT_SUPPORT_COORDINATOR (Backfill subsoil cavity & lay compacted bitumen)",
        "rule_applied": "UTILITY_EROSION_PRECEDENCE",
        "rule_rationale": "Active pressurized drinking water pipeline burst is the root cause of ground subsidence. Water board must isolate valve and repair pipeline before Road crew can backfill and compact asphalt.",
        "primary_sla_ack": "5 Minutes (Demo Policy)",
        "primary_sla_res": "2 Hours (Water Isolation & Pipeline Splicing)",
        "secondary_sla_ack": "15 Minutes",
        "secondary_sla_res": "6 Hours (Sub-base Compaction & Resurfacing)",
        "decline_simulation": {
            "dept": "Water Supply Board (MWSSB)",
            "officer": "Er. T. Chandran (Executive Engineer)",
            "quote": "This complaint was reported as a road crater / pothole. Public road repairs belong exclusively to Roads & Infrastructure Department.",
            "intercept_msg": "Ping-pong bounce blocked. Ground cavitation is water-induced. Escalated to Zonal Commissioner.",
            "directive_id": "JD-2026-906"
        }
    },
    {
        "id": "case4",
        "tab_label": "Case 4: Uprooted Tree (Horticulture vs Roads)",
        "badge": "TRANSIT OBSTRUCTION PRECEDENCE",
        "title": "Uprooted 15-Ton Banyan Tree Blocking Highway",
        "location": "Anna Salai Arterial Highway Border (Ward 140 / Ward 141 Border)",
        "coords": "13.0112° N, 80.2185° E",
        "input_img": "input_raw_case4_fallen_tree.jpg",
        "workflow_card": "workflow_case_4_fallen_tree_road.jpg",
        "hazard_type": "FALLEN_TREE_ROAD",
        "description": "Massive 15-ton uprooted banyan tree collapsed completely across both carriageway lanes, crushing concrete median barrier and blocking traffic.",
        "conflict_type": "TRANSIT_OBSTRUCTION_AND_ROAD_DAMAGE",
        "primary_dept": "Horticulture & Tree Authority (HORT)",
        "primary_role": "LEAD_RESPONDER (Mobilize chainsaw crews & hydraulic crane to section timber)",
        "secondary_dept": "Roads & Infrastructure Department (ROADS)",
        "secondary_role": "JOINT_SUPPORT_COORDINATOR (Rebuild crushed concrete median barrier & sweep road)",
        "rule_applied": "TRANSIT_OBSTRUCTION_PRECEDENCE",
        "rule_rationale": "Physical tree trunk and debris obstruction must be cut and removed by Horticulture woodcutters before Road Department can rebuild damaged divider kerb.",
        "primary_sla_ack": "10 Minutes",
        "primary_sla_res": "2 Hours (Tree Sectioning & Lane Clearance)",
        "secondary_sla_ack": "30 Minutes",
        "secondary_sla_res": "5 Hours (Median Barrier Reconstruction)",
        "decline_simulation": {
            "dept": "Horticulture Authority (HORT)",
            "officer": "Dr. R. Natarajan (Tree Officer)",
            "quote": "The median barrier is crushed and major vehicular arterial transit is blocked. Roads Department and Traffic Authority must divert and handle.",
            "intercept_msg": "Rejection intercepted. Tree Authority has legal custody of felled botanical timber. Escalated to Commissioner.",
            "directive_id": "JD-2026-907"
        }
    },
    {
        "id": "case5",
        "tab_label": "Case 5: Refuse in Canal (Solid Waste vs Drainage)",
        "badge": "DEBRIS CLEARANCE PRECEDENCE",
        "title": "Commercial Garbage Dumping in Storm Drainage Canal",
        "location": "Outer Ring Boundary Canal Road (Ward 85 / Ward 86 Border)",
        "coords": "13.0694° N, 80.1948° E",
        "input_img": "input_raw_case5_garbage_canal.jpg",
        "workflow_card": "workflow_case_5_garbage_in_drain.jpg",
        "hazard_type": "GARBAGE_IN_DRAIN",
        "description": "5 tons of illegally dumped commercial packaging, plastic sacks, and municipal refuse completely clogging storm drainage culvert intake mouth.",
        "conflict_type": "GARBAGE_BLOCKING_STORM_DRAIN",
        "primary_dept": "Solid Waste Management Department (SWM)",
        "primary_role": "LEAD_RESPONDER (Deploy mechanical grab compactor & dumpers to scoop garbage)",
        "secondary_dept": "Stormwater Drainage & Flood Mitigation (SWD)",
        "secondary_role": "JOINT_SUPPORT_COORDINATOR (Desilt culvert interior once mouth surface refuse cleared)",
        "rule_applied": "DEBRIS_CLEARANCE_PRECEDENCE",
        "rule_rationale": "External dumped commercial refuse and garbage must be cleared by Solid Waste compactors before Drainage department can desilt the interior canal bed.",
        "primary_sla_ack": "15 Minutes",
        "primary_sla_res": "2 Hours (Mechanical Refuse Extraction)",
        "secondary_sla_ack": "30 Minutes",
        "secondary_sla_res": "4 Hours (Interior Silt Removal)",
        "decline_simulation": {
            "dept": "Solid Waste Management (SWM)",
            "officer": "Shri M. Velu (Sanitary Inspector)",
            "quote": "The refuse is located inside the culvert channel. Canal cleaning and desilting falls strictly under Stormwater Drainage Department.",
            "intercept_msg": "Ping-pong bounce blocked. Solid waste compaction equipment required. Escalated to Joint Commissioner.",
            "directive_id": "JD-2026-908"
        }
    }
]

def build_html():
    cases_json = json.dumps(SHOWCASE_DATA)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Problem 3: Multi-Department Conflict Engine & Anti-Ping-Pong Routing Showcase</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {{
      --bg: #0b1120;
      --card-bg: #1e293b;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary-green: #10b981;
      --secondary-blue: #3b82f6;
      --accent-red: #ef4444;
      --accent-amber: #f59e0b;
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-family);
      line-height: 1.5;
      padding: 24px;
    }}
    .header {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }}
    .header h1 {{
      font-size: 26px;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .header p {{
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 6px;
    }}
    .badge-pill {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}
    .badge-success {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}
    .badge-info {{ background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }}
    .badge-warn {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}

    /* Tabs Navigation */
    .tabs-nav {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 12px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }}
    .tab-btn {{
      background: #1e293b;
      color: var(--text-muted);
      border: 1px solid var(--border);
      padding: 10px 18px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{ background: #334155; color: #fff; }}
    .tab-btn.active {{
      background: #0284c7;
      color: #fff;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }}

    /* Main Showcase Grid */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 24px;
    }}
    @media (max-width: 1100px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .preview-img {{
      width: 100%;
      height: 380px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid var(--border);
      margin-bottom: 14px;
      background: #0f172a;
    }}
    .meta-row {{
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      margin-bottom: 8px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      padding-bottom: 6px;
    }}
    .meta-label {{ color: var(--text-muted); font-weight: 600; }}
    .meta-val {{ color: var(--text); font-weight: 500; text-align: right; }}

    /* Workflow Pipeline Stepper */
    .stepper {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 14px;
    }}
    .step-item {{
      display: flex;
      gap: 12px;
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      align-items: flex-start;
    }}
    .step-num {{
      background: #0284c7;
      color: #fff;
      font-weight: 800;
      font-size: 12px;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .step-content h4 {{ font-size: 13px; font-weight: 700; margin-bottom: 4px; }}
    .step-content p {{ font-size: 12px; color: var(--text-muted); }}

    /* Live SLA Timers */
    .sla-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 16px 0;
    }}
    .sla-box {{
      padding: 14px;
      border-radius: 8px;
      border: 1px solid;
    }}
    .sla-primary {{
      background: rgba(16, 185, 129, 0.1);
      border-color: rgba(16, 185, 129, 0.4);
    }}
    .sla-secondary {{
      background: rgba(59, 130, 246, 0.1);
      border-color: rgba(59, 130, 246, 0.4);
    }}
    .sla-box h5 {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
    .sla-timer {{
      font-family: monospace;
      font-size: 24px;
      font-weight: 800;
      color: #fbbf24;
    }}

    /* Simulation Control Deck */
    .sim-deck {{
      background: #0f172a;
      border: 2px dashed #475569;
      border-radius: 10px;
      padding: 18px;
      margin-top: 18px;
    }}
    .sim-deck h3 {{
      font-size: 14px;
      color: #38bdf8;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .btn-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .btn {{
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }}
    .btn-decline {{ background: #dc2626; color: #fff; }}
    .btn-decline:hover {{ background: #b91c1c; }}
    .btn-timeout {{ background: #d97706; color: #fff; }}
    .btn-timeout:hover {{ background: #b45309; }}
    .btn-ack {{ background: #16a34a; color: #fff; }}
    .btn-ack:hover {{ background: #15803d; }}
    .btn-reset {{ background: #475569; color: #fff; }}
    .btn-reset:hover {{ background: #334155; }}

    /* Event Output Log Banner */
    .event-log {{
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 14px;
      font-family: monospace;
      font-size: 12px;
      min-height: 80px;
      overflow-y: auto;
      max-height: 180px;
    }}
    .log-danger {{ color: #f87171; }}
    .log-warn {{ color: #fbbf24; }}
    .log-success {{ color: #34d399; }}
    .log-info {{ color: #38bdf8; }}

    /* Full Workflow Composite Embed */
    .full-card-section {{
      margin-top: 24px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }}
    .full-card-img {{
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      display: block;
    }}
  </style>
</head>
<body>

  <div class="header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
      <div>
        <h1>
          <span>🏛️</span>
          Municipal Multi-Department Conflict Resolution Engine
        </h1>
        <p>Problem 3 Solution Demonstration: Ward Boundary Ambiguities, Statutory Root-Cause Precedence, Dual SLAs & Anti-Ping-Pong Dispute Lock</p>
      </div>
      <div style="display: flex; gap: 8px;">
        <span class="badge-pill badge-danger">5-Min Demo SLA Enforced</span>
        <span class="badge-pill badge-success">Anti-Ping-Pong Active</span>
        <span class="badge-pill badge-info">100% Evaluation Passed</span>
      </div>
    </div>
  </div>

  <!-- Tabs Navigation -->
  <div class="tabs-nav" id="tabsNav"></div>

  <!-- Main Grid for Selected Case -->
  <div class="grid-2">
    <!-- Left: Input Picture & Geo-Telematics -->
    <div class="card">
      <div class="card-title">
        <span id="caseTitle">Incident Telemetry & Input Picture</span>
        <span id="caseBadge" class="badge-pill badge-danger"></span>
      </div>
      <img id="caseInputImg" class="preview-img" src="" alt="Input Raw Civic Photo">
      
      <div class="meta-row">
        <span class="meta-label">Arterial Location:</span>
        <span class="meta-val" id="caseLocation"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">GPS Telemetry:</span>
        <span class="meta-val" id="caseCoords" style="color: #38bdf8; font-family: monospace;"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Ward Boundary Status:</span>
        <span class="meta-val" style="color: #fbbf24; font-weight: 700;">CONFIRMED INTER-WARD BORDER</span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Citizen Complaint:</span>
        <span class="meta-val" id="caseDesc" style="font-style: italic; max-width: 60%;"></span>
      </div>
    </div>

    <!-- Right: AI Precedence & Interactive Simulation Deck -->
    <div class="card">
      <div class="card-title">
        <span>AI Conflict Engine & SLA Clocks</span>
        <span class="badge-pill badge-success" id="caseRule"></span>
      </div>

      <!-- Precedence & Department Mandates -->
      <div style="background: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 14px;">
        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Statutory Pre-Assignment:</div>
        <div style="font-size: 13px; margin-top: 4px;">
          <span style="color: #34d399; font-weight: 700;">Lead Responder:</span> <span id="casePrimaryDept"></span>
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-left: 12px;" id="casePrimaryRole"></div>
        <div style="font-size: 13px; margin-top: 6px;">
          <span style="color: #60a5fa; font-weight: 700;">Joint Partner:</span> <span id="caseSecondaryDept"></span>
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-left: 12px;" id="caseSecondaryRole"></div>
        <div style="font-size: 12px; margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
          <strong style="color: #fbbf24;">Precedence Rationale:</strong> <span id="caseRationale" style="color: #cbd5e1;"></span>
        </div>
      </div>

      <!-- Dual SLA Timers -->
      <div class="sla-container">
        <div class="sla-box sla-primary">
          <h5 style="color: #34d399;">Primary SLA (Lead Responder)</h5>
          <div class="sla-timer" id="slaTimerPrimary">04:59</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Policy: 5m Ack | Res: <span id="primaryResLimit"></span></div>
          <div style="font-size: 11px; font-weight: 700; color: #34d399;" id="primarySlaStatus">CLOCK RUNNING</div>
        </div>
        <div class="sla-box sla-secondary">
          <h5 style="color: #60a5fa;">Secondary SLA (Joint Support)</h5>
          <div class="sla-timer" style="color: #60a5fa;" id="slaTimerSecondary">14:59</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Policy: 15m Ack | Res: <span id="secondaryResLimit"></span></div>
          <div style="font-size: 11px; font-weight: 700; color: #60a5fa;" id="secondarySlaStatus">STANDBY COORDINATION</div>
        </div>
      </div>

      <!-- Simulation Action Deck -->
      <div class="sim-deck">
        <h3>
          <span>⚙️</span> Interactive Problem 3 Event Simulator
        </h3>
        <p style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">Test how the backend engine prevents ping-pong routing and enforces supervisor escalations in real-time:</p>
        
        <div class="btn-row">
          <button class="btn btn-decline" onclick="simulateDecline()">
            <span>🚫</span> Dept A Declines ("Not Our Job")
          </button>
          <button class="btn btn-timeout" onclick="simulateTimeout()">
            <span>⏱️</span> 5-Min SLA Timeout
          </button>
          <button class="btn btn-ack" onclick="simulateAck()">
            <span>✅</span> Lead Officer Acknowledges
          </button>
          <button class="btn btn-reset" onclick="resetSim()">
            <span>🔄</span> Reset
          </button>
        </div>

        <div class="event-log" id="simLog">
          <span class="log-info">[SYSTEM INITIALIZED]</span> Case loaded into Municipal Operations Engine.<br>
          <span class="log-info">[SLA ENGINE]</span> 5-minute critical safety acknowledgment clock ticking.<br>
          Ready for interactive test simulation.
        </div>
      </div>
    </div>
  </div>

  <!-- Full Composite Workflow Visual Card Embed -->
  <div class="full-card-section">
    <div class="card-title">
      <span>High-Resolution Operations Console Card (Full Workflow Output)</span>
      <span class="badge-pill badge-info">1600 x 960 Composite</span>
    </div>
    <img id="caseFullCardImg" class="full-card-img" src="" alt="Full Composite Card">
  </div>

  <script>
    const cases = {cases_json};
    let currentIdx = 0;
    let timerInterval = null;
    let secondsLeft = 299; // 5 mins demo timer

    function initTabs() {{
      const nav = document.getElementById("tabsNav");
      nav.innerHTML = "";
      cases.forEach((c, idx) => {{
        const btn = document.createElement("button");
        btn.className = "tab-btn " + (idx === 0 ? "active" : "");
        btn.innerText = c.tab_label;
        btn.onclick = () => selectCase(idx);
        nav.appendChild(btn);
      }});
      selectCase(0);
    }}

    function selectCase(idx) {{
      currentIdx = idx;
      const allBtns = document.querySelectorAll(".tab-btn");
      allBtns.forEach((b, i) => b.className = "tab-btn " + (i === idx ? "active" : ""));

      const c = cases[idx];
      document.getElementById("caseTitle").innerText = c.title;
      document.getElementById("caseBadge").innerText = c.badge;
      document.getElementById("caseInputImg").src = c.input_img;
      document.getElementById("caseLocation").innerText = c.location;
      document.getElementById("caseCoords").innerText = c.coords;
      document.getElementById("caseDesc").innerText = '"' + c.description + '"';

      document.getElementById("caseRule").innerText = c.rule_applied;
      document.getElementById("casePrimaryDept").innerText = c.primary_dept;
      document.getElementById("casePrimaryRole").innerText = c.primary_role;
      document.getElementById("caseSecondaryDept").innerText = c.secondary_dept;
      document.getElementById("caseSecondaryRole").innerText = c.secondary_role;
      document.getElementById("caseRationale").innerText = c.rule_rationale;

      document.getElementById("primaryResLimit").innerText = c.primary_sla_res;
      document.getElementById("secondaryResLimit").innerText = c.secondary_sla_res;

      document.getElementById("caseFullCardImg").src = c.workflow_card;

      resetSim();
    }}

    function startTimer() {{
      if (timerInterval) clearInterval(timerInterval);
      secondsLeft = 299;
      updateTimerDisplay();
      timerInterval = setInterval(() => {{
        if (secondsLeft > 0) {{
          secondsLeft--;
          updateTimerDisplay();
        }} else {{
          clearInterval(timerInterval);
          simulateTimeout();
        }}
      }}, 1000);
    }}

    function updateTimerDisplay() {{
      const m = Math.floor(secondsLeft / 60);
      const s = secondsLeft % 60;
      document.getElementById("slaTimerPrimary").innerText = 
        String(m).padStart(2, '0') + ":" + String(s).padStart(2, '0');
    }}

    function simulateDecline() {{
      const c = cases[currentIdx];
      const log = document.getElementById("simLog");
      const d = c.decline_simulation;

      log.innerHTML += `<br><span class="log-danger">[UNILATERAL REASSIGNMENT ATTEMPT]</span> ` +
        `<strong>${{d.officer}} (${{d.dept}})</strong> attempted to decline:<br>` +
        `<em>"${{d.quote}}"</em><br>` +
        `<span class="log-warn">[PING-PONG SHIELD INTERCEPTED]</span> Reassignment to secondary department <strong>BLOCKED</strong>.<br>` +
        `<span class="log-danger">[SUPERVISOR ESCALATION]</span> Ticket escalated directly to <strong>Zonal Joint Municipal Commissioner</strong>.<br>` +
        `<span class="log-success">[ENFORCEMENT]</span> Binding <strong>MANDATORY JOINT TASK DIRECTIVE #${{d.directive_id}}</strong> issued. Both crews ordered to site concurrently under Commissioner Oversight.`;
      
      log.scrollTop = log.scrollHeight;
      document.getElementById("primarySlaStatus").innerHTML = "<span style='color: #ef4444;'>DISPUTE INTERCEPTED & ESCALATED</span>";
    }}

    function simulateTimeout() {{
      if (timerInterval) clearInterval(timerInterval);
      document.getElementById("slaTimerPrimary").innerText = "00:00";
      const log = document.getElementById("simLog");
      log.innerHTML += `<br><span class="log-danger">[SLA CLOCK BREACHED]</span> 5-minute demonstration acknowledgment deadline elapsed without officer response.<br>` +
        `<span class="log-warn">[HIGH COMMAND SIREN TRIGGERED]</span> Auto-escalated to Municipal Commissioner Control Room for immediate punitive dispatch!`;
      log.scrollTop = log.scrollHeight;
      document.getElementById("primarySlaStatus").innerHTML = "<span style='color: #ef4444;'>SLA BREACH - AUTO-ESCALATED</span>";
    }}

    function simulateAck() {{
      if (timerInterval) clearInterval(timerInterval);
      const log = document.getElementById("simLog");
      log.innerHTML += `<br><span class="log-success">[SLA STOPPED - ACKNOWLEDGED]</span> Lead responder acknowledged within safety window.<br>` +
        `<span class="log-info">[DISPATCH ACTIVE]</span> Mobile response crew en route. ETA 12 minutes.`;
      log.scrollTop = log.scrollHeight;
      document.getElementById("primarySlaStatus").innerHTML = "<span style='color: #10b981;'>ACKNOWLEDGED - CREW ON ROUTE</span>";
    }}

    function resetSim() {{
      startTimer();
      document.getElementById("primarySlaStatus").innerText = "CLOCK RUNNING";
      document.getElementById("simLog").innerHTML = 
        `<span class="log-info">[SYSTEM INITIALIZED]</span> Case loaded into Municipal Operations Engine.<br>` +
        `<span class="log-info">[SLA ENGINE]</span> 5-minute critical safety acknowledgment clock ticking.<br>` +
        `Ready for interactive test simulation.`;
    }}

    document.addEventListener("DOMContentLoaded", initTabs);
  </script>
</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Interactive HTML Showcase created successfully at: {HTML_PATH}")
    return HTML_PATH

if __name__ == "__main__":
    build_html()
