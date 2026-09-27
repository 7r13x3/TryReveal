import asyncio
import aiohttp
import socket
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
)

from tryreveal.core.loader import load_map, load_rules
from tryreveal.core.url_builder import build_urls
from tryreveal.verifiers.generic import fetch as http_fetch, score_generic, HEADERS
from tryreveal.verifiers.rule_engine import score_with_rule, needs_browser
from tryreveal import logger

console = logger.console


async def scan_domain(target, cfg, db):
    logger.info(f"Domain: {target}")

    # Pre-check: does the domain resolve?
    try:
        ip = socket.gethostbyname(target)
        logger.success(f"Domain resolves to: {ip}")
    except Exception:
        logger.warn(f"Domain {target} does NOT resolve — results may be limited.")
        ip = None

    logger.info("Loading OSINT map...")
    data = load_map(cfg.username.map_path)

    # Only scan the "Domain Name" branch of the map
    domain_branch = None
    for child in data.get("children", []):
        if child.get("name", "").lower() == "domain name":
            domain_branch = child
            break

    if not domain_branch:
        logger.warn("No 'Domain Name' branch found in the map.")
        return {"total": 0, "confirmed": 0, "hits": []}

    urls = build_urls(domain_branch, target)
    rules = load_rules() if cfg.username.use_rules else {}

    logger.info(f"Loaded {len(urls)} domain-specific URLs.")
    logger.info(f"Rules loaded: {len(rules)}")

    http_jobs = []
    browser_jobs = []

    for u in urls:
        rule = rules.get(u["url"])
        if needs_browser(rule) and cfg.browser.enabled:
            browser_jobs.append((u, rule))
        else:
            http_jobs.append((u, rule))

    logger.info(f"HTTP jobs:    {len(http_jobs)}")
    logger.info(f"Browser jobs: {len(browser_jobs)}")

    run_id = db.start_run("domain", target)
    results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Verifying"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("scan", total=len(urls))

        sem = asyncio.Semaphore(cfg.scan.concurrency)
        connector = aiohttp.TCPConnector(limit=cfg.scan.concurrency, ssl=False)

        async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
            async def http_worker(item, rule):
                async with sem:
                    raw = await http_fetch(session, item["url"], cfg.scan.timeout)
                    if rule:
                        confirmed, conf, reason = score_with_rule(raw, rule)
                    else:
                        confirmed, conf, reason = score_generic(raw)
                    item.update({
                        "status": raw["status"], "confirmed": confirmed,
                        "confidence": conf, "reason": reason, "engine": "http",
                    })
                    db.add_hit(run_id, item["name"], item["url"],
                               raw["status"], conf, reason, confirmed)
                    results.append(item)
                    progress.advance(task)

            await asyncio.gather(*(http_worker(u, r) for u, r in http_jobs))

    confirmed = [r for r in results if r["confirmed"]]
    confirmed.sort(key=lambda x: -x["confidence"])

    logger.success(f"Scan complete. {len(confirmed)}/{len(results)} confirmed.")
    logger.hits_table(confirmed)

    result = {
        "run_id": run_id, "target": target, "ip": ip,
        "total": len(results), "confirmed": len(confirmed),
        "hits": confirmed,
    }
    if ip:
        result["resolved_ip"] = ip
    return result
