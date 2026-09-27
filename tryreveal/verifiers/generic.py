import aiohttp

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}

NEGATIVE_HINTS = [
    "user not found", "page not found", "doesn't exist", "does not exist",
    "sorry, this page isn't available", "account suspended", "no user",
    "not a valid", "was not found", "could not find", "profile not found",
    "this account doesn't exist", "404 not found", "no such user",
]


async def fetch(session, url, timeout):
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            allow_redirects=True,
        ) as resp:
            body = (await resp.text(errors="ignore"))[:30000].lower()
            return {"status": resp.status, "body": body}
    except Exception:
        return {"status": "error", "body": ""}


def score_generic(result):
    status = result["status"]
    body = result["body"]

    if status == "error":
        return False, 0, "network"

    has_negative = any(h in body for h in NEGATIVE_HINTS)

    if status in (200, 201):
        if has_negative:
            return False, 10, "negative-signal"
        return True, 50, "200-clean"
    if status in (301, 302, 307, 308):
        return True, 60, "redirect"
    if status == 403:
        return True, 40, "forbidden"
    if status == 404:
        return False, 0, "404"
    return False, 0, f"status-{status}"
