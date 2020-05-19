from pathlib import Path

sqlite3_path = Path(__file__).parents[2] / 'dev_local_db.sqlite3'

DEV_DB_CONFIG = {
    'dev': {
        'driver': 'sqlite',
        'database': sqlite3_path,
    }
}
