<div align="center">

# 🎯 TryReveal

### *Try triangulate — You're the third point*

**Autonomous OSINT agent that scans 1,500+ tools in seconds.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Playwright](https://img.shields.io/badge/Playwright-1.40-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](https://github.com/7r13x3/TryReveal/pulls)

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Usage](#-usage) • [Roadmap](#-roadmap) • [Legal](#-legal-disclaimer)

</div>

---

## 🧠 What is TryReveal?

**TryReveal** is a self-hosted OSINT (Open-Source Intelligence) reconnaissance engine. Give it a **username**, **email**, **phone number**, **domain**, or **IP** — it fires concurrent requests across **1,500+ online tools** and returns only the **confirmed hits**.

Instead of visiting hundreds of websites manually, TryReveal does it in **~15 seconds**.
┌──────────────────┐
│ You type: │
│ "Try wizzard" │
└────────┬─────────┘
│
┌────────▼─────────────────────────┐
│ TryReveal Engine │
│ ───────────────────────────── │
│ • Loads arf.json (1,500 tools) │
│ • Injects target into URLs │
│ • Fires 100 async requests │
│ • Verifies page content │
│ • Auto-learns site rules │
└────────┬─────────────────────────┘
│
┌────────▼─────────┐
│ Confirmed Hits │
│ ─────────────── │
│ ✓ GitHub │
│ ✓ Reddit │
│ ✓ Keybase │
│ ✓ ... 47 more │
└──────────────────┘

---

## ✨ Features

| Feature | Description |
|---|---|
|  **Multi-Input Scan** | Username, Email, Phone, Domain, IP/MAC |
|  **Async Engine** | 100 concurrent requests via `aiohttp` |
|  **Auto-Learn Rules** | Probes each site with fake usernames to build detection rules |
|  **Browser Verifier** | Playwright + stealth for JavaScript-heavy sites |
|  **TLS Spoofing** | `curl_cffi` mimics real Chrome fingerprint for Cloudflare bypass |
|  **Beautiful Output** | Rich terminal UI + color-coded confirmed hits |
|  **Web Dashboard** | FastAPI-powered browser interface |
|  **SQLite Storage** | Every scan and hit is persisted for later analysis |
|  **Multi-Export** | JSON, CSV, and HTML report generation |
|  **Plugin Architecture** | Add new modules without touching core code |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/7r13x3/TryReveal.git
cd TryReveal
2. Install dependencies
pip install -r requirements.txt
playwright install chromium
3. Run the CLI
⚖️ Legal Disclaimer
TryReveal is provided for authorized security testing only.

Only scan targets you own or have written permission to test.

Unauthorized scanning, harvesting, or reconnaissance is illegal in most jurisdictions.

The authors assume no liability for misuse.

Respect each target site's Terms of Service.
📜 License
Distributed under the MIT License. See LICENSE for details.
🌟 Star History
If TryReveal helped you, drop a ⭐ on the repo — it means a lot!

https://api.star-history.com/svg?repos=7r13x3/TryReveal&type=Date

<div align="center">
Built with ❤️ by @7r13x3

Try triangulate You're the third point.

</div> ```
