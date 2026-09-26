import sys
from dataclasses import dataclass, field
from tryreveal.core.paths import DEFAULT_CONFIG

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class ScanCfg:
    timeout: int = 8
    concurrency: int = 100
    user_agent: str = "TryReveal/1.0 (OSINT)"


@dataclass
class UsernameCfg:
    map_path: str = "data/arf.json"
    rules_path: str = "data/rules.json"
    use_rules: bool = True


@dataclass
class EmailCfg:
    verify_domain: bool = True


@dataclass
class PhoneCfg:
    default_region: str = "US"


@dataclass
class IpCfg:
    use_internetdb: bool = True


@dataclass
class BrowserCfg:
    enabled: bool = True
    concurrency: int = 5
    timeout: int = 20
    headless: bool = True
    proxy: str = ""


@dataclass
class ExportCfg:
    default_format: str = "json"


@dataclass
class Config:
    scan: ScanCfg = field(default_factory=ScanCfg)
    username: UsernameCfg = field(default_factory=UsernameCfg)
    email: EmailCfg = field(default_factory=EmailCfg)
    phone: PhoneCfg = field(default_factory=PhoneCfg)
    ip: IpCfg = field(default_factory=IpCfg)
    browser: BrowserCfg = field(default_factory=BrowserCfg)
    export: ExportCfg = field(default_factory=ExportCfg)


def load(path: str = None) -> Config:
    path = path or str(DEFAULT_CONFIG)
    with open(path, "rb") as f:
        data = tomllib.load(f)

    def _get(s, k, d):
        return data.get(s, {}).get(k, d)

    return Config(
        scan=ScanCfg(
            timeout=int(_get("scan", "timeout", 8)),
            concurrency=int(_get("scan", "concurrency", 100)),
            user_agent=_get("scan", "user_agent", "TryReveal/1.0 (OSINT)"),
        ),
        username=UsernameCfg(
            map_path=_get("username", "map_path", "data/arf.json"),
            rules_path=_get("username", "rules_path", "data/rules.json"),
            use_rules=bool(_get("username", "use_rules", True)),
        ),
        email=EmailCfg(verify_domain=bool(_get("email", "verify_domain", True))),
        phone=PhoneCfg(default_region=_get("phone", "default_region", "US")),
        ip=IpCfg(use_internetdb=bool(_get("ip", "use_internetdb", True))),
        browser=BrowserCfg(
            enabled=bool(_get("browser", "enabled", True)),
            concurrency=int(_get("browser", "concurrency", 5)),
            timeout=int(_get("browser", "timeout", 20)),
            headless=bool(_get("browser", "headless", True)),
            proxy=_get("browser", "proxy", ""),
        ),
        export=ExportCfg(default_format=_get("export", "default_format", "json")),
    )
