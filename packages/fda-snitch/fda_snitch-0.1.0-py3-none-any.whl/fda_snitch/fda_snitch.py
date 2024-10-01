import hashlib
import sqlite3
import time
import urllib.request
from datetime import datetime
from pathlib import Path

create_table = """
    CREATE TABLE IF NOT EXISTS logs (
        id integer PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        connected integer,
        hash text
    ); """

class Snitch:
    def __init__(self, sleep=2, database_path=None, url=None):
        conn = None
        self.sleep = sleep
        self.uri = "./log.sqlite" if database_path is None else database_path
        self.url = "https://google.com" if url is None else url

        try:
            conn, cursor = self._connect_db()
            cursor.execute(create_table)
        finally:
            if conn:
                conn.close()

    def _connect_db(self):
        conn = sqlite3.connect(self.uri)
        return conn, conn.cursor()

    def _ping(self):
        try:
            response = urllib.request.urlopen(self.url)
            response.read() # probably not necessary
            return True
        except urllib.error.URLError:
            return False
        except Exception:
            return False

    def run_snitch(self):
        conn, cursor = self._connect_db()
        while(True):
            time.sleep(self.sleep)

            # create hash of file
            with open(Path(__file__).resolve(),"rb") as f:
                hash = hashlib.md5(f.read()).hexdigest()
            
            # current timestamp
            now = datetime.now()

            # try to reach out to google.nl
            connected = int(self._ping())

            # inject in database
            cursor.execute(f"""
                         INSERT INTO logs (timestamp, connected, hash)
                         VALUES 
                         ('{now}', {connected}, '{hash}')
                         """)
            conn.commit()
