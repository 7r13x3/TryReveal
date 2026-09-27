import asyncio
from playwright.async_api import async_playwright

try:
    from playwright_stealth import stealth_async
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

from tryreveal import logger


DEFAULT_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-setuid-sandbox",
    "--window-size=1920,1080",
]


class BrowserPool:
    def __init__(self, concurrency=5, headless=True, user_agent=None, proxy=None):
        self.concurrency = concurrency
        self.headless = headless
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        self.proxy = proxy
        self._playwright = None
        self._browser = None
        self._sem = asyncio.Semaphore(concurrency)

    async def start(self):
        self._playwright = await async_playwright().start()
        opts = {"headless": self.headless, "args": DEFAULT_ARGS}
        if self.proxy:
            opts["proxy"] = {"server": self.proxy}
        self._browser = await self._playwright.chromium.launch(**opts)
        logger.info(f"Browser pool started (concurrency={self.concurrency})")

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def fetch(self, url, timeout=15):
        async with self._sem:
            context = await self._browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
            )
            page = await context.new_page()
            if HAS_STEALTH:
                await stealth_async(page)

            try:
                response = await page.goto(
                    url, wait_until="domcontentloaded", timeout=timeout * 1000
                )
                await asyncio.sleep(1.5)
                body = await page.content()
                return {
                    "status": response.status if response else 0,
                    "body": body.lower(),
                    "final_url": page.url,
                }
            except Exception as e:
                return {"status": "error", "body": "", "error": str(e)}
            finally:
                await context.close()


_pool = None
_lock = asyncio.Lock()


async def get_pool(concurrency=5, proxy=None):
    global _pool
    async with _lock:
        if _pool is None:
            _pool = BrowserPool(concurrency=concurrency, proxy=proxy)
            await _pool.start()
    return _pool


async def shutdown_pool():
    global _pool
    if _pool is not None:
        await _pool.stop()
        _pool = None
