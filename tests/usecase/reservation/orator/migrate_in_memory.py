from pathlib import Path

from orator import DatabaseManager
from orator.migrations import DatabaseMigrationRepository, Migrator

TEST_DB_CONFIG = {
    'test': {
        'driver': 'sqlite',
        'database': ':memory:'
    }
}


def migrate_in_memory(database_manager: DatabaseManager):
    """
    参考: https://github.com/sdispater/orator/issues/159#issuecomment-288464538
    """
    migration_repository = DatabaseMigrationRepository(database_manager, 'migrations')
    migrator = Migrator(migration_repository, database_manager)

    if not migrator.repository_exists():
        migration_repository.create_repository()

    migrations_path = Path(__file__).parents[4] / 'migrations'
    migrator.run(migrations_path)
