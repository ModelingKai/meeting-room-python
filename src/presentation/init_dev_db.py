from orator import Schema, DatabaseManager
from orator.schema import Blueprint

DEV_DB_CONFIG = {
    'dev': {
        'driver': 'sqlite',
        'database': 'dev_db.sqlite3',
    }
}


def init_dev_db():
    schema = Schema(DatabaseManager(DEV_DB_CONFIG))

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
