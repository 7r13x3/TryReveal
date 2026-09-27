import asyncio
import aiohttp
from tryreveal.verifiers.generic import HEADERS, fetch


def looks_like_js_site(body):
    if len(body) < 2000:
        return True
    js_markers = ["__next", "__nuxt", "react-root", "ng-version", "v-app"]
    return any(m in body for m in js_markers)


async def learn_site(session, site, timeout=8):
    r1 = await fetch(session, site["url"], timeout)
    r2 = await fetch(session, site["url"], timeout)
    if not r1["body"] or not r2["body"]:
        return None

    needs_js = looks_like_js_site(r1["body"])

    lines1 = set(r1["body"].splitlines())
    lines2 = set(r2["body"].splitlines())
    stable = lines1 & lines2

    negatives = []
    for line in sorted(stable, key=len, reverse=True):
        line = line.strip()
        if 10 < len(line) < 120 and "<" not in line:
            negatives.append(line[:100])
        if len(negatives) >= 3:
            break

    return {
        "positive": [],
        "negative": negatives,
        "requires_js": needs_js,
        "source": "auto-learned",
    }


async def learn_all(sites, concurrency=20, timeout=8):
    rules = {}
    sem = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)

    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        async def worker(site):
            async with sem:
                rule = await learn_site(session, site, timeout)
                if rule:
                    rules[site["url"]] = rule
        await asyncio.gather(*(worker(s) for s in sites))
    return rules
