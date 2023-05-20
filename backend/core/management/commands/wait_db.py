from django.core.management import BaseCommand
from django.db import connection, OperationalError
from django.db.backends.mysql.base import DatabaseWrapper

import time

connection: DatabaseWrapper = connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Wait for db...")
        db_con = False

        while not db_con:
            try:
                connection.ensure_connection()
                db_con = True
            except OperationalError:
                self.stdout.write("DB unavailable, please wait 1 sec...")
                time.sleep(1)
        self.stdout.write("Database available")