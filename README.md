# TryReveal

> Try triangulate — You're the third point — scans 1,500+ tools

TryReveal is an autonomous OSINT agent that checks one identifier (username, email, phone, IP) across ~1,500 tools in seconds.

## Features

- Interactive CLI menu (Username / Email / Phone / IP)
- Web dashboard (FastAPI)
- Async concurrent scanning (100 requests at once)
- Auto-learns site rules — no hand-written rules needed
- Playwright integration for JavaScript-heavy sites
- Confirmed hits only — no false positives
- Export to JSON / CSV / HTML
- SQLite storage for scan history

## Install

```bash
git clone https://github.com/YOUR_USERNAME/TryReveal.git
cd TryReveal
pip install -r requirements.txt
playwright install chromium
