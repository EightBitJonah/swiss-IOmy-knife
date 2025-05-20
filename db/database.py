import sqlite3
import os

class Database:
    def __init__(self, db_name):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_api_keys_table()

    def _create_api_keys_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                access_key TEXT NOT NULL,
                secret_key TEXT NOT NULL
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

    def close(self):
        self.connection.close()