import socket
from tryreveal import logger


async def scan_email(target, cfg, db):
    logger.info(f"Email: {target}")
    domain = target.split("@")[-1]

    resolves = False
    try:
        socket.gethostbyname(domain)
        resolves = True
    except Exception:
        pass

    run_id = db.start_run("email", target)

    if resolves:
        logger.success(f"Domain {domain} resolves.")
    else:
        logger.warn(f"Domain {domain} does NOT resolve.")

    return {
        "run_id": run_id, "target": target, "domain": domain,
        "resolves": resolves, "total": 0, "confirmed": 0, "hits": [],
    }
