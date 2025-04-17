import time
from psycopg2 import OperationalError as Psycopg2Operation
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.db import connections

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for the database...')
        db_running = False 
        while db_running is False:
            try:
                connections['default'].cursor()
                print('Cursor fetched!')
                db_running = True
            except (OperationalError, Psycopg2Operation):
                self.stdout.write('Database is not ready yet. waiting...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is running! Running the server...'))
        