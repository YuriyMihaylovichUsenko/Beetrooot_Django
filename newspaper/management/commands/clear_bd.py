from django.core.management.base import BaseCommand, CommandError
from newspaper.cleaner_db import main

class Command(BaseCommand):
    help = 'cleaning data'

    def handle(self, *args, **options):

        try:
            main()
            print('All tables in mydatabase are empty')
        except Exception:
            raise CommandError('Error cleaning')

        self.stdout.write(self.style.SUCCESS('Successfully cleaning'))
