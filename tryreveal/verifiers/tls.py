try:
    from curl_cffi.requests import AsyncSession
    HAS_CURL = True
except ImportError:
    HAS_CURL = False


IMPERSONATE = "chrome120"


async def fetch_tls(url, timeout=15):
    if not HAS_CURL:
        return {"status": "error", "body": "", "error": "curl_cffi not installed"}
    try:
        async with AsyncSession(impersonate=IMPERSONATE) as session:
            r = await session.get(url, timeout=timeout, allow_redirects=True)
            body = r.text[:50000].lower() if r.text else ""
            return {"status": r.status_code, "body": body, "final_url": str(r.url)}
    except Exception as e:
        return {"status": "error", "body": "", "error": str(e)}
