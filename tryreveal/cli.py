import asyncio
import argparse
from rich.prompt import Prompt, Confirm

from tryreveal import __version__, logger
from tryreveal.config import load
from tryreveal.db import DB
from tryreveal.modules import username, email, phone, ip, domain
from tryreveal.core.loader import load_map, save_rules
from tryreveal.core.url_builder import build_urls
from tryreveal.learning.auto_rules import learn_all
from tryreveal.exporters import json_export, csv_export, html_export


MENU = {
    "1": ("Username", "username"),
    "2": ("Email", "email"),
    "3": ("Phone", "phone"),
    "4": ("IP / MAC", "ip"),
    "5": ("Domain", "domain"),
    "6": ("Learn rules for all sites (one-time)", "learn"),
    "0": ("Exit", "exit"),
}


def menu(cfg):
    db = DB()
    while True:
        logger.banner()
        for k, (label, _) in MENU.items():
            logger.console.print(f"  [bold white][{k}][/bold white] {label}")
        logger.console.print()

        choice = Prompt.ask("[?] Select a category",
                            choices=list(MENU.keys()), default="1")
        label, action = MENU[choice]

        if action == "exit":
            logger.console.print("[yellow]Goodbye.[/yellow]")
            break

        if action == "learn":
            asyncio.run(_learn(cfg))
            Prompt.ask("\n  Press ENTER to return", default="")
            continue

        target = Prompt.ask(f"[?] Enter the {label.lower()} to search").strip()
        if not target:
            continue

        if action == "username":
            results = asyncio.run(username.scan_username(target, cfg, db))
        elif action == "email":
            results = asyncio.run(email.scan_email(target, cfg, db))
        elif action == "phone":
            results = phone.scan_phone(target, cfg, db)
        elif action == "ip":
            results = asyncio.run(ip.scan_ip(target, cfg, db))
        elif action == "domain":
            results = asyncio.run(domain.scan_domain(target, cfg, db))
        else:
            continue

        fmt = Prompt.ask(
            "[?] Export? [json/csv/html/none]",
            choices=["json", "csv", "html", "none"],
            default=cfg.export.default_format,
        )
        if fmt == "json":
            logger.success(json_export.export(results, target))
        elif fmt == "csv":
            logger.success(csv_export.export(results, target))
        elif fmt == "html":
            logger.success(html_export.export(results, target))

        if results.get("hits") and Confirm.ask("[?] Open confirmed hits?", default=False):
            import webbrowser
            for h in results["hits"]:
                url = h.get("url")
                if url:
                    webbrowser.open(url)

        Prompt.ask("\n  Press ENTER to return to menu", default="")

    db.close()


async def _learn(cfg):
    data = load_map(cfg.username.map_path)
    urls = build_urls(data, "zzqqxx9999notrealzz")
    logger.info(f"Learning rules for {len(urls)} sites...")
    rules = await learn_all(urls, concurrency=20, timeout=8)
    save_rules(rules)
    logger.success(f"Saved {len(rules)} rules to data/rules.json")


def main():
    parser = argparse.ArgumentParser(prog="tryreveal")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument("--config", "-c", default="configs/example.toml")
    parser.add_argument("--mode", choices=["username", "email", "phone", "ip", "domain", "learn"])
    parser.add_argument("--target", "-t")
    args = parser.parse_args()

    cfg = load(args.config)

    if args.mode and args.target:
        db = DB()
        if args.mode == "username":
            asyncio.run(username.scan_username(args.target, cfg, db))
        elif args.mode == "email":
            asyncio.run(email.scan_email(args.target, cfg, db))
        elif args.mode == "phone":
            phone.scan_phone(args.target, cfg, db)
        elif args.mode == "ip":
            asyncio.run(ip.scan_ip(args.target, cfg, db))
        elif args.mode == "domain":
            asyncio.run(domain.scan_domain(args.target, cfg, db))
        db.close()
        return

    menu(cfg)


if __name__ == "__main__":
    main()
