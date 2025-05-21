import sqlite3
import os

class Database:
    def __init__(self, db_name):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                access_key TEXT NOT NULL,
                secret_key TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nmap_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def store_api_key(self, service, access_key, secret_key):
        self.cursor.execute('''
            INSERT OR REPLACE INTO api_keys (service, access_key, secret_key)
            VALUES (?, ?, ?)
        ''', (service, access_key, secret_key))
        self.connection.commit()

    def get_api_key(self, service):
        self.cursor.execute('''
            SELECT access_key, secret_key FROM api_keys WHERE service = ?
        ''', (service,))
        return self.cursor.fetchone()

    def store_nmap_targets(self, scan_id, targets):
        """Store a list of IP addresses found by nmap for a specific scan"""
        self.cursor.executemany('''
            INSERT INTO nmap_targets (scan_id, target_ip)
            VALUES (?, ?)
        ''', [(scan_id, ip.strip()) for ip in targets])
        self.connection.commit()

    def get_nmap_targets(self, scan_id):
        """Get all targets for a specific scan"""
        self.cursor.execute('''
            SELECT target_ip FROM nmap_targets 
            WHERE scan_id = ?
            ORDER BY timestamp DESC
        ''', (scan_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def delete_nmap_targets(self, scan_id):
        """Delete all targets for a specific scan after they've been processed"""
        self.cursor.execute('''
            DELETE FROM nmap_targets 
            WHERE scan_id = ?
        ''', (scan_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()