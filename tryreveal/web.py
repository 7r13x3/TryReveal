from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from tryreveal.config import load
from tryreveal.db import DB
from tryreveal.modules import username, email, phone, ip, domain

app = FastAPI(title="TryReveal")
cfg = load()


HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<title>TryReveal</title>
<style>
body{background:#0d1117;color:#c9d1d9;font-family:system-ui;padding:40px;max-width:900px;margin:auto}
h1{color:#58a6ff;text-align:center;font-size:42px;letter-spacing:2px;margin-bottom:8px}
.sub{text-align:center;color:#8b949e;margin-bottom:30px;font-size:15px;font-style:italic}
form{display:flex;gap:10px;margin-bottom:30px}
select,input{padding:12px;background:#161b22;border:1px solid #30363d;color:#c9d1d9;border-radius:6px;font-size:15px}
select{width:180px} input{flex:1}
button{padding:12px 24px;background:#238636;color:white;border:none;border-radius:6px;cursor:pointer;font-weight:bold}
button:hover{background:#2ea043}
.hit{background:#161b22;border:1px solid #30363d;padding:12px;border-radius:6px;margin-bottom:8px}
.hit a{color:#58a6ff;text-decoration:none}
.hit a:hover{text-decoration:underline}
.stats{text-align:center;color:#8b949e;margin-bottom:20px;font-size:15px}
</style></head><body>
<h1>TryReveal</h1>
<p class="sub">Try triangulate — You're the third point — scans 1,500+ tools</p>
<form id="f">
  <select id="mode">
    <option value="username">Username</option>
    <option value="email">Email</option>
    <option value="phone">Phone</option>
    <option value="ip">IP / MAC</option>
    <option value="domain">Domain</option>
  </select>
  <input id="target" placeholder="Enter target..." required>
  <button type="submit">Scan</button>
</form>
<div class="stats" id="stats"></div>
<div id="results"></div>
<script>
document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const target = document.getElementById('target').value.trim();
  const mode = document.getElementById('mode').value;
  if(!target) return;
  document.getElementById('results').innerHTML = '<p style="text-align:center;color:#58a6ff">Scanning...</p>';
  const res = await fetch('/scan', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({mode, target})
  });
  const data = await res.json();
  document.getElementById('stats').innerHTML =
    `<b style="color:#3fb950">${data.confirmed}</b> confirmed / ${data.total} scanned`;
  document.getElementById('results').innerHTML = '';
  data.hits.forEach((h,i) => {
    const d = document.createElement('div');
    d.className = 'hit';
    d.innerHTML = `<b>${i+1}. ${h.name}</b> <span style="color:#8b949e">(${h.status||''} · ${h.confidence||0}%)</span><br>
                   <a href="${h.url||'#'}" target="_blank">${h.url||''}</a>`;
    document.getElementById('results').appendChild(d);
  });
};
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.post("/scan")
async def scan(payload: dict):
    mode = payload.get("mode", "username")
    target = payload.get("target", "").strip()
    if not target:
        return JSONResponse({"error": "no target"}, status_code=400)

    db = DB()
    try:
        if mode == "username":
            r = await username.scan_username(target, cfg, db)
        elif mode == "email":
            r = await email.scan_email(target, cfg, db)
        elif mode == "phone":
            r = phone.scan_phone(target, cfg, db)
        elif mode == "ip":
            r = await ip.scan_ip(target, cfg, db)
        elif mode == "domain":
            r = await domain.scan_domain(target, cfg, db)
        else:
            return JSONResponse({"error": "bad mode"}, status_code=400)
    finally:
        db.close()

    return {
        "target": target,
        "total": r.get("total", 0),
        "confirmed": r.get("confirmed", 0),
        "hits": r.get("hits", []),
    }
