import sqlite3
from tryreveal.core.paths import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT, target TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS hits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER, name TEXT, url TEXT,
    status TEXT, confidence INTEGER, reason TEXT, confirmed INTEGER
);
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT, country TEXT, region TEXT,
    carrier TEXT, line_type TEXT
);
"""


class DB:
    def __init__(self, path: str = None):
        self.path = path or str(DB_PATH)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def start_run(self, mode, target):
        cur = self.conn.execute(
            "INSERT INTO runs (mode, target) VALUES (?, ?)", (mode, target)
        )
        self.conn.commit()
        return cur.lastrowid

    def add_hit(self, run_id, name, url, status, confidence, reason, confirmed):
        self.conn.execute(
            "INSERT INTO hits (run_id, name, url, status, confidence, reason, confirmed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (run_id, name, url, str(status), confidence, reason, int(confirmed)),
        )
        self.conn.commit()

    def add_phone(self, number, country="", region="", carrier="", line_type=""):
        self.conn.execute(
            "INSERT INTO phones (number, country, region, carrier, line_type) "
            "VALUES (?, ?, ?, ?, ?)",
            (number, country, region, carrier, line_type),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
