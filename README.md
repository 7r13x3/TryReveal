# TryReveal

**Autonomous OSINT agent that scans 1,500+ tools in seconds.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Playwright](https://img.shields.io/badge/Playwright-1.40-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What is TryReveal?

**TryReveal** is a self-hosted OSINT reconnaissance engine. Give it a **username**, **email**, **phone number**, **domain**, or **IP** — it fires concurrent requests across **1,500+ online tools** and returns only the **confirmed hits**.

Instead of visiting hundreds of websites manually, TryReveal does it in **~15 seconds**.

---

## Features

| Feature | Description |
|---|---|
| **Multi-Input Scan** | Username, Email, Phone, Domain, IP/MAC |
| **Async Engine** | 100 concurrent requests via `aiohttp` |
| **Auto-Learn Rules** | Probes each site with fake usernames to build detection rules |
| **Browser Verifier** | Playwright + stealth for JavaScript-heavy sites |
| **TLS Spoofing** | `curl_cffi` mimics real Chrome fingerprint for Cloudflare bypass |
| **Beautiful Output** | Rich terminal UI + color-coded confirmed hits |
| **Web Dashboard** | FastAPI-powered browser interface |
| **SQLite Storage** | Every scan and hit is persisted for later analysis |
| **Multi-Export** | JSON, CSV, and HTML report generation |

---

## Quick Start

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

