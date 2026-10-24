"""
Interactive HTML Showcase Builder for Municipal Monsoon Heavy Rain Dual-Engine Evaluation
Renders side-by-side interactive viewer with:
- Engine 1: Privacy Redaction Before/After (Raw, Proof, Blur, Blackbox)
- Engine 2: Department Assignment, Precedence Rule, Dual SLAs, and Anti-Ping-Pong Shield
"""

import os
import json

ARTIFACT_DIR = r"C:\Users\Lenovo\.gemini\antigravity\brain\82af6ceb-bb74-4b65-8996-16630260df13"
HTML_PATH = os.path.join(ARTIFACT_DIR, "monsoon_dual_engine_comparison.html")
JSON_PATH = os.path.join(ARTIFACT_DIR, "monsoon_dual_engine_results.json")

def build_html():
    if not os.path.exists(JSON_PATH):
        print(f"Missing {JSON_PATH}")
        return None

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    cases_json = json.dumps(cases)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Problem Statement Monsoon Heavy Rain: Dual Backend Engine Comparison</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {{
      --bg: #0b1120;
      --card-bg: #1e293b;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent-cyan: #38bdf8;
      --accent-green: #10b981;
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
      font-size: 24px;
      font-weight: 700;
      color: var(--accent-cyan);
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
    .badge-monsoon {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }}
    .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}
    .badge-success {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}

    /* Tabs */
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

    /* Grid 2 Columns for Dual Engines */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 24px;
    }}
    @media (max-width: 1200px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }}
    .card-title {{
      font-size: 17px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Mode Controls for Engine 1 */
    .view-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }}
    .mode-btn {{
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid var(--border);
      background: #0f172a;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .mode-btn:hover {{ background: #334155; color: #fff; }}
    .mode-btn.active {{
      background: #0284c7;
      color: #fff;
      border-color: #38bdf8;
    }}

    .preview-box {{
      width: 100%;
      height: 380px;
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 14px;
    }}
    .preview-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
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

    /* Dual SLA Box */
    .sla-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 14px 0;
    }}
    .sla-box {{
      padding: 12px;
      border-radius: 8px;
      border: 1px solid;
    }}
    .sla-lead {{
      background: rgba(16, 185, 129, 0.1);
      border-color: rgba(16, 185, 129, 0.4);
    }}
    .sla-joint {{
      background: rgba(59, 130, 246, 0.1);
      border-color: rgba(59, 130, 246, 0.4);
    }}
    .sla-box h5 {{ font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }}
    .sla-time {{ font-size: 20px; font-weight: 800; font-family: monospace; color: #fbbf24; }}

    /* Interactive Decline Simulation */
    .sim-banner {{
      background: #0f172a;
      border: 1px dashed #ef4444;
      border-radius: 8px;
      padding: 14px;
      margin-top: 14px;
    }}
    .sim-btn {{
      padding: 8px 14px;
      background: #dc2626;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .sim-btn:hover {{ background: #b91c1c; }}

    /* Full Composite Card Section */
    .full-comp-section {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }}
    .full-comp-img {{
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
  </style>
</head>
<body>

  <div class="header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
      <div>
        <h1>
          <span>🌧️</span>
          Problem Statement Heavy Rain: Dual Backend Engine Comparison
        </h1>
        <p>Real-Time Evaluation on Municipal Monsoon Deluge Photos: Backend Engine 1 (Privacy Redactor) & Backend Engine 2 (Department Assignment & Ping-Pong Shield)</p>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="badge-pill badge-monsoon">Heavy Rain Deluge</span>
        <span class="badge-pill badge-danger">5-Min Demo SLA Clock</span>
        <span class="badge-pill badge-success">Anti-Ping-Pong Enforced</span>
      </div>
    </div>
  </div>

  <!-- Tabs Navigation -->
  <div class="tabs-nav" id="tabsNav"></div>

  <!-- Dual Column Grid -->
  <div class="grid-2">
    <!-- Left: Backend Engine 1 (Privacy Redaction) -->
    <div class="card">
      <div class="card-title">
        <span style="color: #38bdf8;">Engine 1: Privacy Redaction & Sanitization</span>
        <span class="badge-pill badge-monsoon" id="eng1Badge"></span>
      </div>

      <div class="view-controls">
        <button class="mode-btn" id="btnRaw" onclick="switchEng1Mode('raw')">📷 1. Raw Input</button>
        <button class="mode-btn active" id="btnProof" onclick="switchEng1Mode('proof')">🎯 2. Detection Proof</button>
        <button class="mode-btn" id="btnBlur" onclick="switchEng1Mode('blur')">💧 3. Gaussian Blur</button>
        <button class="mode-btn" id="btnBb" onclick="switchEng1Mode('blackbox')">⬛ 4. Blackbox</button>
      </div>

      <div class="preview-box">
        <img id="eng1Img" src="" alt="Engine 1 Output">
      </div>

      <div class="meta-row">
        <span class="meta-label">Inference Latency:</span>
        <span class="meta-val" id="eng1Latency" style="color: #38bdf8; font-weight:700;"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Total Redactions:</span>
        <span class="meta-val" id="eng1Total" style="color: #34d399; font-weight:700;"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Faces Sanitized:</span>
        <span class="meta-val" id="eng1Faces"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">License Plates Sanitized:</span>
        <span class="meta-val" id="eng1Plates"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Phone Numbers / Digits:</span>
        <span class="meta-val" id="eng1Digits"></span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Camera EXIF Metadata:</span>
        <span class="meta-val" style="color: #34d399; font-weight:700;">STRIPPED (Zero GPS Leakage)</span>
      </div>
    </div>

    <!-- Right: Backend Engine 2 (Department Assignment & Problem 3 Precedence) -->
    <div class="card">
      <div class="card-title">
        <span style="color: #34d399;">Engine 2: Department Assignment & Precedence</span>
        <span class="badge-pill badge-success" id="eng2Rule"></span>
      </div>

      <div style="background: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 12px;">
        <div style="font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Jurisdictional Boundary:</div>
        <div style="font-size: 13px; font-weight: 700; color: #fbbf24;" id="eng2Ward"></div>
        <div style="font-size: 12px; color: #cbd5e1; margin-top: 2px;" id="eng2Road"></div>
        <div style="font-size: 12px; color: #38bdf8; font-family: monospace;" id="eng2Coords"></div>
      </div>

      <div style="background: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 12px;">
        <div style="font-size: 13px;">
          <strong style="color: #34d399;">Lead Responder:</strong> <span id="eng2Primary"></span>
        </div>
        <div style="font-size: 13px; margin-top: 4px;">
          <strong style="color: #60a5fa;">Joint Support:</strong> <span id="eng2Secondary"></span>
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
          <strong style="color: #fbbf24;">Precedence Rationale:</strong> <span id="eng2Rationale" style="color: #cbd5e1;"></span>
        </div>
      </div>

      <!-- Dual SLA Clocks -->
      <div class="sla-row">
        <div class="sla-box sla-lead">
          <h5 style="color: #34d399;">Primary SLA (Lead Responder)</h5>
          <div class="sla-time" id="eng2SlaTimer">04:59</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Policy: 5m Ack | Res: <span id="eng2PrimaryRes"></span></div>
          <div style="font-size: 11px; font-weight: 700; color: #34d399;" id="eng2PrimaryStatus">ACTIVE COUNTDOWN</div>
        </div>
        <div class="sla-box sla-joint">
          <h5 style="color: #60a5fa;">Secondary SLA (Joint Support)</h5>
          <div class="sla-time" style="color: #60a5fa;">14:59</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Policy: 15m Ack | Res: <span id="eng2SecondaryRes"></span></div>
          <div style="font-size: 11px; font-weight: 700; color: #60a5fa;">STANDBY DISPATCH</div>
        </div>
      </div>

      <!-- Interactive Anti-Ping-Pong Simulator -->
      <div class="sim-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <strong style="color: #f87171; font-size: 13px;">Test Ping-Pong Rejection Interception:</strong>
          <button class="sim-btn" onclick="triggerDecline()">🚫 Simulate Dept A Decline</button>
        </div>
        <div id="simLog" style="font-size: 12px; font-family: monospace; color: #94a3b8;">
          Click "Simulate Dept A Decline" to test how the engine blocks reassignment and escalates to the Commissioner.
        </div>
      </div>
    </div>
  </div>

  <!-- Full Composite 1600x960 Card -->
  <div class="full-comp-section">
    <div class="card-title">
      <span>Unified 1600x960 Composite Operations Card</span>
      <span class="badge-pill badge-monsoon">Dual Engine Output</span>
    </div>
    <img id="fullCompImg" class="full-comp-img" src="" alt="Full Composite">
  </div>

  <script>
    const cases = {cases_json};
    let currentIdx = 0;
    let eng1Mode = 'proof';

    function init() {{
      const nav = document.getElementById("tabsNav");
      nav.innerHTML = "";
      cases.forEach((c, idx) => {{
        const btn = document.createElement("button");
        btn.className = "tab-btn " + (idx === 0 ? "active" : "");
        btn.innerText = c.title.split(":")[0];
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
      // Engine 1
      document.getElementById("eng1Badge").innerText = c.engine1_telemetry.total_redactions + " Targets";
      document.getElementById("eng1Latency").innerText = c.engine1_telemetry.latency_ms + " ms";
      document.getElementById("eng1Total").innerText = c.engine1_telemetry.total_redactions;
      document.getElementById("eng1Faces").innerText = c.engine1_telemetry.faces_redacted;
      document.getElementById("eng1Plates").innerText = c.engine1_telemetry.plates_redacted;
      document.getElementById("eng1Digits").innerText = c.engine1_telemetry.numbers_redacted;

      // Engine 2
      document.getElementById("eng2Rule").innerText = c.engine2_routing.rule_applied;
      document.getElementById("eng2Ward").innerText = c.ward;
      document.getElementById("eng2Road").innerText = c.road_name;
      document.getElementById("eng2Coords").innerText = c.coords;
      document.getElementById("eng2Primary").innerText = c.engine2_routing.primary_dept + " [" + c.engine2_routing.primary_code + "]";
      document.getElementById("eng2Secondary").innerText = c.engine2_routing.secondary_dept + " [" + c.engine2_routing.secondary_code + "]";
      document.getElementById("eng2Rationale").innerText = c.engine2_routing.rationale;
      document.getElementById("eng2PrimaryRes").innerText = c.engine2_routing.primary_res_limit_hr + "h";
      document.getElementById("eng2SecondaryRes").innerText = c.engine2_routing.secondary_res_limit_hr + "h";

      document.getElementById("fullCompImg").src = c.composite_file;

      document.getElementById("simLog").innerHTML = 'Click "Simulate Dept A Decline" to test how the engine blocks reassignment and escalates to the Commissioner.';
      document.getElementById("eng2PrimaryStatus").innerText = "ACTIVE COUNTDOWN";
      document.getElementById("eng2PrimaryStatus").style.color = "#34d399";

      updateEng1Display();
    }}

    function switchEng1Mode(mode) {{
      eng1Mode = mode;
      document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
      if (mode === 'raw') document.getElementById("btnRaw").classList.add("active");
      if (mode === 'proof') document.getElementById("btnProof").classList.add("active");
      if (mode === 'blur') document.getElementById("btnBlur").classList.add("active");
      if (mode === 'blackbox') document.getElementById("btnBb").classList.add("active");
      updateEng1Display();
    }}

    function updateEng1Display() {{
      const c = cases[currentIdx];
      const img = document.getElementById("eng1Img");
      if (eng1Mode === 'raw') img.src = c.raw_file;
      else if (eng1Mode === 'proof') img.src = c.proof_file;
      else if (eng1Mode === 'blur') img.src = c.blur_file;
      else if (eng1Mode === 'blackbox') img.src = c.blackbox_file;
    }}

    function triggerDecline() {{
      const c = cases[currentIdx];
      const sim = c.decline_simulation;
      const log = document.getElementById("simLog");
      log.innerHTML = `<span style="color:#f87171;">[DECLINE ATTEMPT]</span> <strong>${{sim.officer}} (${{sim.declining_dept}})</strong>:<br>` +
        `<em>"${{sim.quote}}"</em><br>` +
        `<span style="color:#fbbf24;">[ANTI-PING-PONG SHIELD]</span> Reassignment to Roads Department <strong>BLOCKED</strong>.<br>` +
        `<span style="color:#f87171;">[SUPERVISOR ESCALATION]</span> Escalated to <strong>Zonal Joint Municipal Commissioner</strong>.<br>` +
        `<span style="color:#34d399;">[DIRECTIVE ISSUED]</span> <strong>MANDATORY JOINT ORDER #JD-2026-904</strong> enforced. Both field teams dispatched concurrently.`;
      document.getElementById("eng2PrimaryStatus").innerText = "DISPUTE ESCALATED TO SUPERVISOR";
      document.getElementById("eng2PrimaryStatus").style.color = "#ef4444";
    }}

    document.addEventListener("DOMContentLoaded", init);
  </script>
</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Interactive Dual-Engine Showcase HTML generated at: {HTML_PATH}")
    return HTML_PATH

if __name__ == "__main__":
    build_html()
