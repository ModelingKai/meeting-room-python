from pathlib import Path

from orator import Schema, DatabaseManager
from orator.schema import Blueprint

sqlite3_path = Path(__file__).parent / 'dev_db.sqlite3'

DEV_DB_CONFIG = {
    'dev': {
        'driver': 'sqlite',
        'database': sqlite3_path,
    }
}


def init_dev_db():
    schema = Schema(DatabaseManager(DEV_DB_CONFIG))

    table_name = 'reservation'
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


def main():
    """
    たぶん、DB初期化あたり、初期化用スクリプト的なやつで1回だけ呼ばれるようにする感じにしそう
    """
    init_dev_db()
    print('Initialized DB')  # 本当は、Loggerでやるべき


if __name__ == '__main__':
    main()
