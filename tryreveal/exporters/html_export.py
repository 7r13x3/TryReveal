from pathlib import Path
from datetime import datetime


def export(results, target):
    safe = target.replace("@", "_at_").replace(".", "_").replace("/", "_")
    path = Path(f"results_{safe}.html")
    hits = results.get("hits", [])
    rows = "\n".join(
        f"<tr><td>{h.get('name','')}</td>"
        f"<td><a href='{h.get('url','')}' target='_blank'>{h.get('url','')}</a></td>"
        f"<td>{h.get('status','')}</td>"
        f"<td>{h.get('confidence',0)}%</td></tr>"
        for h in hits
    )
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>TryReveal — {target}</title>
<style>
body{{background:#0d1117;color:#c9d1d9;font-family:system-ui;padding:24px}}
h1{{color:#58a6ff}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #30363d;padding:8px;text-align:left}}
th{{background:#161b22}}a{{color:#58a6ff}}
</style></head><body>
<h1>TryReveal Report</h1>
<p><b>Target:</b> {target}</p>
<p><b>Generated:</b> {datetime.utcnow().isoformat()}Z</p>
<p><b>Confirmed:</b> {len(hits)}</p>
<table><tr><th>Tool</th><th>URL</th><th>Status</th><th>Confidence</th></tr>
{rows}</table></body></html>"""
    path.write_text(html, encoding="utf-8")
    return str(path)
