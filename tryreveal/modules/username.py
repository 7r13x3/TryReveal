import asyncio
import aiohttp
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
)

from tryreveal.core.loader import load_map, load_rules
from tryreveal.core.url_builder import build_urls
from tryreveal.verifiers.generic import fetch as http_fetch, score_generic, HEADERS
from tryreveal.verifiers.rule_engine import score_with_rule, needs_browser
from tryreveal import logger

console = logger.console


async def scan_username(target, cfg, db):
    logger.info(f"Target: {target}")
    logger.info("Loading OSINT map...")

    data = load_map(cfg.username.map_path)
    urls = build_urls(data, target)
    rules = load_rules() if cfg.username.use_rules else {}

    logger.info(f"Loaded {len(urls)} checkable URLs.")
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

    run_id = db.start_run("username", target)
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

    return {
        "run_id": run_id, "target": target,
        "total": len(results), "confirmed": len(confirmed),
        "hits": confirmed,
    }
