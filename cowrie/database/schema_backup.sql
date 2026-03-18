CREATE TABLE ssh_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    src_ip TEXT,
    username TEXT,
    password TEXT,
    command TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE web_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    src_ip TEXT,
    username TEXT,
    password TEXT,
    endpoint TEXT
);
CREATE TABLE attack_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src_ip TEXT,
    country TEXT,
    attack_type TEXT,
    risk_score INTEGER
);
