from pathlib import Path

from orator import DatabaseManager, Schema
from orator.schema import Blueprint

root_path = Path(__file__).parents[2]
sqlite3_file_path = root_path / 'orator_db.sqlite3'

DB_CONFIG = {
    'development': {
        'driver': 'sqlite',
        'database': sqlite3_file_path,
    }
}


def main():
    db = DatabaseManager(DB_CONFIG)
    schema = Schema(db)

    table_name = 'reservations'
    schema.drop_if_exists(table_name)

    with schema.create(table_name) as table:
        table: Blueprint

        table.string('id').unique()
        table.string('meeting_room_id')
        table.string('reserver_id')
        table.enum('reservation_status', ['予約中', 'キャンセル済み'])
        table.integer('number_of_participants')
        table.datetime('start_datetime')
        table.datetime('end_datetime')

        table.datetime('created_at')
        table.datetime('updated_at')


if __name__ == '__main__':
    main()
