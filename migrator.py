import uuid

import click
from peewee_moves import DatabaseManager

from utils.models.base import conn

manager = DatabaseManager(conn)


@click.group()
def main() -> None:
    pass


@main.command()
def makemigrations():
    manager.revision(str(uuid.uuid4()).replace('-', '_'))


@main.command()
def migrate():
    manager.upgrade()


@main.command()
@click.option('--migration-name', '-m', required=True)
def rollback(migration_name):
    manager.downgrade(migration_name)


if __name__ == '__main__':
    main()
