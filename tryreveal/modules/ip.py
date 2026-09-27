import aiohttp
from tryreveal import logger


async def scan_ip(target, cfg, db):
    logger.info(f"IP/MAC: {target}")
    result = {"target": target}
    run_id = db.start_run("ip", target)

    if cfg.ip.use_internetdb:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"https://internetdb.shodan.io/{target}",
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        result.update(data)
                        logger.success("InternetDB data received.")
        except Exception as e:
            logger.warn(f"InternetDB failed: {e}")

    return {"run_id": run_id, "target": target, "total": 1,
            "confirmed": 1, "hits": [result]}
