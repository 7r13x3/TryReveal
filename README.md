#  TryReveal

###

**Autonomous OSINT agent that scans 1,500+ tools in seconds.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Playwright](https://img.shields.io/badge/Playwright-1.40-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🧠 What is TryReveal?

**TryReveal** is a self-hosted OSINT reconnaissance engine. Give it a **username**, **email**, **phone number**, **domain**, or **IP** — it fires concurrent requests across **1,500+ online tools** and returns only the **confirmed hits**.

Instead of visiting hundreds of websites manually, TryReveal does it in **~15 seconds**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Multi-Input Scan** | Username, Email, Phone, Domain, IP/MAC |
| ⚡ **Async Engine** | 100 concurrent requests via `aiohttp` |
| 🧠 **Auto-Learn Rules** | Probes each site with fake usernames to build detection rules |
| 🌐 **Browser Verifier** | Playwright + stealth for JavaScript-heavy sites |
| 🔒 **TLS Spoofing** | `curl_cffi` mimics real Chrome fingerprint for Cloudflare bypass |
| 📊 **Beautiful Output** | Rich terminal UI + color-coded confirmed hits |
| 🌍 **Web Dashboard** | FastAPI-powered browser interface |
| 💾 **SQLite Storage** | Every scan and hit is persisted for later analysis |
| 📤 **Multi-Export** | JSON, CSV, and HTML report generation |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/7r13x3/TryReveal.git
cd TryReveal
2. Install dependencies
bash
pip install -r requirements.txt
playwright install chromium
3. Run the CLI
bash
python -m tryreveal.cli
🛣️ Roadmap
☑ v1.0 — Username/Email/Phone/IP/Domain scanning
☑ v1.0 — Auto-learn rules engine
☑ v1.0 — Web dashboard
□ v1.1 — Full Playwright integration
□ v1.2 — Residential proxy rotation
□ v1.3 — Neo4j entity graph
□ v1.4 — Local LLM analysis via Ollama
□ v2.0 — Multi-user SaaS with auth
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit your changes: git commit -m "Add amazing feature"

Push: git push origin feature/amazing-feature

Open a Pull Request

⚖️ Legal Disclaimer
TryReveal is provided for authorized security testing only.

Only scan targets you own or have written permission to test.

Unauthorized scanning is illegal in most jurisdictions.

The authors assume no liability for misuse.

📜 License
Distributed under the MIT License. See LICENSE for details.

🙏 Credits
OSINT Framework by Justin Nordine — the source map that powers this project

Rich — terminal UI

FastAPI — backend

Playwright browser automation

Built with ❤️ by @7r13x3
