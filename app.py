from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import models
from environment import EmailEnv, SAMPLE_EMAILS, TASKS

app = FastAPI(title="EmailTriagePro - OpenEnv", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = EmailEnv()

HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>EmailTriagePro — AI Email Triage Environment</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0d0f14;
    --surface: #161921;
    --surface2: #1e2230;
    --border: #2a2f3e;
    --accent: #7c6df0;
    --accent2: #5eead4;
    --accent3: #f59e0b;
    --text: #e8eaf0;
    --muted: #7a8099;
    --spam: #ef4444;
    --urgent: #f97316;
    --technical: #3b82f6;
    --hr: #a78bfa;
    --billing: #f59e0b;
    --support: #10b981;
    --general: #6b7280;
    --radius: 12px;
    --font: 'Sora', sans-serif;
    --mono: 'JetBrains Mono', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    min-height: 100vh;
    line-height: 1.6;
  }

  /* Top Nav */
  nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 32px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
    backdrop-filter: blur(12px);
  }
  .logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 18px; font-weight: 700; letter-spacing: -0.3px;
  }
  .logo-icon {
    width: 32px; height: 32px; background: var(--accent);
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-size: 16px;
  }
  .nav-badge {
    background: var(--accent); color: #fff;
    font-size: 11px; padding: 3px 10px; border-radius: 20px;
    font-weight: 600; letter-spacing: 0.5px;
  }

  /* Layout */
  .layout {
    display: grid;
    grid-template-columns: 300px 1fr 340px;
    gap: 0;
    height: calc(100vh - 61px);
  }

  /* Sidebar */
  .sidebar {
    background: var(--surface);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 20px 16px;
  }
  .sidebar-title {
    font-size: 11px; font-weight: 600; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 12px; padding: 0 4px;
  }
  .email-item {
    padding: 12px 14px;
    border-radius: var(--radius);
    cursor: pointer;
    margin-bottom: 6px;
    border: 1px solid transparent;
    transition: all 0.15s;
  }
  .email-item:hover { background: var(--surface2); border-color: var(--border); }
  .email-item.active { background: rgba(124,109,240,0.12); border-color: var(--accent); }
  .email-sender {
    font-size: 12px; color: var(--muted); margin-bottom: 4px;
    font-family: var(--mono); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .email-subject {
    font-size: 13px; font-weight: 500; color: var(--text);
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    margin-bottom: 6px;
  }
  .cat-badge {
    display: inline-block; font-size: 10px; font-weight: 600;
    padding: 2px 8px; border-radius: 20px; text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .cat-Spam { background: rgba(239,68,68,0.15); color: var(--spam); }
  .cat-Urgent { background: rgba(249,115,22,0.15); color: var(--urgent); }
  .cat-Technical { background: rgba(59,130,246,0.15); color: var(--technical); }
  .cat-HR { background: rgba(167,139,250,0.15); color: var(--hr); }
  .cat-Billing { background: rgba(245,158,11,0.15); color: var(--billing); }
  .cat-Support { background: rgba(16,185,129,0.15); color: var(--support); }
  .cat-General { background: rgba(107,114,128,0.15); color: var(--general); }

  /* Main Area */
  .main {
    display: flex; flex-direction: column;
    overflow-y: auto;
    background: var(--bg);
  }
  .main-header {
    padding: 24px 32px 0;
  }
  .main-header h2 {
    font-size: 22px; font-weight: 700; margin-bottom: 4px;
  }
  .main-header p { color: var(--muted); font-size: 14px; }

  .email-card {
    margin: 20px 32px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
  }
  .email-card-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
  }
  .email-card-subject {
    font-size: 18px; font-weight: 600; margin-bottom: 10px;
  }
  .email-meta {
    display: flex; gap: 16px; flex-wrap: wrap;
  }
  .meta-chip {
    display: flex; align-items: center; gap: 6px;
    font-size: 12px; color: var(--muted);
    font-family: var(--mono);
  }
  .email-card-body {
    padding: 24px;
    font-size: 15px; color: #c8cad8; line-height: 1.8;
  }

  /* Triage Panel */
  .triage-section {
    margin: 0 32px 32px;
  }
  .triage-title {
    font-size: 13px; font-weight: 600; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;
  }
  .triage-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
    margin-bottom: 16px;
  }
  .triage-group label {
    display: block; font-size: 12px; font-weight: 600;
    color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;
  }
  select, .action-btn {
    width: 100%; padding: 10px 14px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-family: var(--font);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border-color 0.15s;
  }
  select:focus, select:hover { border-color: var(--accent); }
  select option { background: var(--surface2); }

  .triage-actions {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;
    margin-bottom: 16px;
  }
  .action-btn {
    padding: 10px 8px; text-align: center; font-weight: 500;
    font-size: 13px; background: var(--surface2);
    border: 1px solid var(--border); border-radius: 10px;
    cursor: pointer; transition: all 0.15s;
  }
  .action-btn:hover { border-color: var(--accent); color: var(--accent); background: rgba(124,109,240,0.08); }
  .action-btn.selected { background: rgba(124,109,240,0.15); border-color: var(--accent); color: var(--accent); }

  .submit-btn {
    width: 100%; padding: 14px;
    background: var(--accent);
    color: #fff; border: none; border-radius: 12px;
    font-family: var(--font); font-size: 15px; font-weight: 600;
    cursor: pointer; transition: all 0.2s;
    letter-spacing: 0.2px;
  }
  .submit-btn:hover { background: #6b5ce7; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(124,109,240,0.3); }
  .submit-btn:active { transform: translateY(0); }
  .submit-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

  /* Result Panel */
  .result-panel {
    border-top: 1px solid var(--border);
    background: var(--surface);
    overflow-y: auto;
    padding: 20px 16px;
  }
  .result-title {
    font-size: 11px; font-weight: 600; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;
  }
  .score-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    margin-bottom: 12px;
  }
  .score-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px;
  }
  .score-email-id { font-size: 12px; color: var(--muted); font-family: var(--mono); }
  .score-value {
    font-size: 24px; font-weight: 700;
    font-family: var(--mono);
  }
  .score-high { color: var(--support); }
  .score-mid { color: var(--accent3); }
  .score-low { color: var(--spam); }

  .score-bar-wrap {
    background: var(--bg); border-radius: 4px; height: 6px; margin-bottom: 10px;
  }
  .score-bar {
    height: 6px; border-radius: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.5s ease;
  }
  .score-row {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; padding: 4px 0;
    border-bottom: 1px solid var(--border);
  }
  .score-row:last-child { border-bottom: none; }
  .score-row-label { color: var(--muted); }
  .correct { color: var(--support); font-weight: 600; }
  .wrong { color: var(--spam); font-weight: 600; }

  .empty-state {
    text-align: center; padding: 40px 16px;
    color: var(--muted); font-size: 13px;
  }
  .empty-icon { font-size: 36px; margin-bottom: 12px; }

  /* Summary stats */
  .stats-row {
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
    margin-bottom: 16px;
  }
  .stat-box {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px;
    text-align: center;
  }
  .stat-val { font-size: 22px; font-weight: 700; font-family: var(--mono); color: var(--accent2); }
  .stat-label { font-size: 11px; color: var(--muted); margin-top: 2px; }

  /* Task selector */
  .task-selector {
    display: flex; gap: 8px; padding: 0 32px; margin: 16px 0 0;
    flex-wrap: wrap;
  }
  .task-pill {
    padding: 7px 16px; border-radius: 20px; font-size: 13px;
    border: 1px solid var(--border); background: var(--surface2);
    cursor: pointer; transition: all 0.15s; font-weight: 500;
  }
  .task-pill:hover { border-color: var(--accent); }
  .task-pill.active { background: var(--accent); border-color: var(--accent); color: #fff; }

  .divider { height: 1px; background: var(--border); margin: 20px 0; }
  .toast {
    position: fixed; bottom: 24px; right: 24px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 20px;
    font-size: 14px; transform: translateY(100px);
    transition: transform 0.3s ease;
    z-index: 999; max-width: 320px;
  }
  .toast.show { transform: translateY(0); }
  .toast.success { border-color: var(--support); }
  .toast.error { border-color: var(--spam); }

  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

  @keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
  .animate-in { animation: fadeIn 0.3s ease; }
</style>
</head>
<body>

<nav>
  <div class="logo">
    <div class="logo-icon">✉</div>
    EmailTriagePro
  </div>
  <div style="display:flex;gap:12px;align-items:center">
    <span style="font-size:13px;color:var(--muted)">OpenEnv v1.0</span>
    <span class="nav-badge">LIVE</span>
  </div>
</nav>

<div class="layout">

  <!-- Sidebar: Email List -->
  <div class="sidebar">
    <div class="sidebar-title">📥 Sample Emails (20)</div>
    <div id="emailList"></div>
  </div>

  <!-- Main: Email Viewer + Triage -->
  <div class="main">
    <div class="main-header">
      <h2>Email Triage Console</h2>
      <p>Classify, prioritize and route emails. Select a task level to begin.</p>
    </div>

    <div class="task-selector">
      <div class="task-pill active" onclick="selectTask('task_1_easy', this)">🟢 Easy — Spam Detection</div>
      <div class="task-pill" onclick="selectTask('task_2_medium', this)">🟡 Medium — Category + Priority</div>
      <div class="task-pill" onclick="selectTask('task_3_hard', this)">🔴 Hard — Full Triage</div>
    </div>

    <div id="emailViewer" style="flex:1">
      <div class="email-card animate-in">
        <div class="email-card-header">
          <div class="email-card-subject" id="emailSubject">Select an email from the sidebar</div>
          <div class="email-meta">
            <div class="meta-chip">📨 <span id="emailSender">—</span></div>
            <div class="meta-chip">🏷 <span id="emailActualCat">—</span></div>
            <div class="meta-chip">⚡ <span id="emailActualPri">—</span></div>
          </div>
        </div>
        <div class="email-card-body" id="emailBody">
          Click any email in the left panel, or start a task to see emails auto-loaded.
        </div>
      </div>

      <!-- Triage Controls -->
      <div class="triage-section">
        <div class="triage-title">⚙ Triage Controls</div>
        <div class="triage-grid">
          <div class="triage-group">
            <label>Category</label>
            <select id="selCategory">
              <option value="">-- Select --</option>
              <option>Spam</option><option>Urgent</option><option>Technical</option>
              <option>HR</option><option>Billing</option><option>Support</option><option>General</option>
            </select>
          </div>
          <div class="triage-group">
            <label>Priority</label>
            <select id="selPriority">
              <option value="">-- Select --</option>
              <option>High</option><option>Medium</option><option>Low</option>
            </select>
          </div>
        </div>
        <div class="triage-title">Routing Action</div>
        <div class="triage-actions" id="actionBtns">
          <div class="action-btn" onclick="selectAction(this,'auto_reply')">💬 Auto Reply</div>
          <div class="action-btn" onclick="selectAction(this,'escalate')">🚨 Escalate</div>
          <div class="action-btn" onclick="selectAction(this,'archive')">🗄 Archive</div>
          <div class="action-btn" onclick="selectAction(this,'forward_to_dev')">⚙ Fwd Dev</div>
          <div class="action-btn" onclick="selectAction(this,'forward_to_billing')">💰 Fwd Billing</div>
          <div class="action-btn" onclick="selectAction(this,'ignore')">🚫 Ignore</div>
        </div>
        <button class="submit-btn" id="submitBtn" onclick="submitTriage()">Submit Triage ↗</button>
      </div>
    </div>
  </div>

  <!-- Right Panel: Results -->
  <div class="result-panel">
    <div class="result-title">📊 Triage Results</div>
    <div class="stats-row">
      <div class="stat-box">
        <div class="stat-val" id="statTotal">0</div>
        <div class="stat-label">Emails Triaged</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" id="statAccuracy">—</div>
        <div class="stat-label">Avg Score</div>
      </div>
    </div>
    <div id="resultsContainer">
      <div class="empty-state">
        <div class="empty-icon">🎯</div>
        Results will appear here after you triage emails.
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const BASE = "";
let allEmails = [];
let currentEmail = null;
let selectedAction = "";
let currentTask = "task_1_easy";
let triageResults = [];
let totalScore = 0;

async function loadEmails() {
  const res = await fetch(BASE + "/emails");
  allEmails = await res.json();
  renderEmailList();
}

function renderEmailList() {
  const el = document.getElementById("emailList");
  el.innerHTML = allEmails.map((e, i) => `
    <div class="email-item" id="item-${i}" onclick="selectEmail(${i})">
      <div class="email-sender">${e.sender}</div>
      <div class="email-subject">${e.subject}</div>
      <span class="cat-badge cat-${e.category}">${e.category}</span>
      <span class="cat-badge" style="background:rgba(255,255,255,0.06);color:var(--muted);margin-left:4px">${e.priority}</span>
    </div>
  `).join("");
}

function selectEmail(i) {
  document.querySelectorAll(".email-item").forEach(el => el.classList.remove("active"));
  document.getElementById("item-" + i).classList.add("active");
  currentEmail = allEmails[i];
  document.getElementById("emailSubject").textContent = currentEmail.subject;
  document.getElementById("emailSender").textContent = currentEmail.sender;
  document.getElementById("emailActualCat").textContent = currentEmail.category;
  document.getElementById("emailActualPri").textContent = currentEmail.priority;
  document.getElementById("emailBody").textContent = currentEmail.body;
}

function selectAction(el, val) {
  document.querySelectorAll(".action-btn").forEach(b => b.classList.remove("selected"));
  el.classList.add("selected");
  selectedAction = val;
}

async function selectTask(taskId, el) {
  document.querySelectorAll(".task-pill").forEach(p => p.classList.remove("active"));
  el.classList.add("active");
  currentTask = taskId;
  triageResults = [];
  totalScore = 0;
  document.getElementById("statTotal").textContent = "0";
  document.getElementById("statAccuracy").textContent = "—";
  document.getElementById("resultsContainer").innerHTML = '<div class="empty-state"><div class="empty-icon">🔄</div>Task reset. Start triaging!</div>';

  const res = await fetch(BASE + "/reset?task_id=" + taskId, { method: "POST" });
  const obs = await res.json();
  if (obs.email_id && obs.email_id !== "done") {
    const emailData = allEmails.find(e => e.id === obs.email_id);
    if (emailData) selectEmail(allEmails.indexOf(emailData));
  }
  showToast("Task loaded: " + taskId, "success");
}

async function submitTriage() {
  if (!currentEmail) { showToast("Select an email first!", "error"); return; }
  const cat = document.getElementById("selCategory").value;
  if (!cat) { showToast("Please select a category.", "error"); return; }

  const btn = document.getElementById("submitBtn");
  btn.disabled = true; btn.textContent = "Processing...";

  const value = cat + "|" + (document.getElementById("selPriority").value || "Low") + "|" + (selectedAction || "auto_reply");
  const payload = { action_type: "full_triage", value };

  try {
    const res = await fetch(BASE + "/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const reward = data.reward;
    const info = data.info || {};

    triageResults.push({ email: currentEmail, reward, info });
    totalScore += reward;
    const avg = totalScore / triageResults.length;

    document.getElementById("statTotal").textContent = triageResults.length;
    document.getElementById("statAccuracy").textContent = (avg * 100).toFixed(1) + "%";

    renderResults();
    showToast("Score: " + (reward * 100).toFixed(0) + "% — " + (reward >= 0.8 ? "✅ Great!" : reward >= 0.4 ? "🟡 Partial" : "❌ Incorrect"), reward >= 0.5 ? "success" : "error");

    if (data.done) {
      showToast("🏁 Task complete! Final score: " + (avg * 100).toFixed(1) + "%", "success");
    } else if (data.observation && data.observation.email_id !== "done") {
      const next = allEmails.find(e => e.id === data.observation.email_id);
      if (next) selectEmail(allEmails.indexOf(next));
    }
  } catch(e) {
    showToast("Error: " + e.message, "error");
  }
  btn.disabled = false; btn.textContent = "Submit Triage ↗";
}

function renderResults() {
  const container = document.getElementById("resultsContainer");
  container.innerHTML = triageResults.slice().reverse().map(r => {
    const sc = r.reward;
    const cls = sc >= 0.8 ? "score-high" : sc >= 0.4 ? "score-mid" : "score-low";
    const bd = r.info.breakdown || {};
    const rows = Object.entries(bd).map(([k, v]) => {
      if (typeof v === "object") {
        const correct = v.score > 0;
        return `<div class="score-row">
          <span class="score-row-label">${k}</span>
          <span>${v.predicted} ${correct ? '<span class="correct">✓</span>' : '<span class="wrong">✗ '+v.actual+'</span>'}</span>
        </div>`;
      }
      return "";
    }).join("");

    return `<div class="score-card animate-in">
      <div class="score-header">
        <div>
          <div class="score-email-id">${r.email.id}</div>
          <div style="font-size:13px;color:var(--text);font-weight:500;margin-top:3px">${r.email.subject.substring(0,40)}...</div>
        </div>
        <div class="score-value ${cls}">${(sc*100).toFixed(0)}%</div>
      </div>
      <div class="score-bar-wrap"><div class="score-bar" style="width:${sc*100}%"></div></div>
      ${rows}
    </div>`;
  }).join("");
}

function showToast(msg, type) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast " + type + " show";
  setTimeout(() => t.className = "toast", 3000);
}

loadEmails();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_UI

@app.get("/emails")
async def get_emails():
    return SAMPLE_EMAILS

@app.get("/tasks")
async def get_tasks():
    return TASKS

@app.post("/reset")
async def reset(task_id: str = "task_1_easy"):
    obs = env.reset(task_id)
    return obs

@app.post("/step")
async def step(action: models.Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state():
    return env.state()

@app.get("/validate")
async def validate():
    return {
        "status": "ok",
        "name": "EmailTriagePro",
        "version": "1.0.0",
        "tasks": list(env.get_tasks().keys()),
        "openenv_compliant": True
    }
