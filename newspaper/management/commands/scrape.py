from django.core.management.base import BaseCommand, CommandError
from newspaper.scraper import main

class Command(BaseCommand):
    help = 'Scraping data for site'

    def handle(self, *args, **options):

        try:
            main()
            print('jaga-jaga-buums')
        except Exception:
            raise CommandError('Error scraping')

        self.stdout.write(self.style.SUCCESS('Successfully scraping'))
