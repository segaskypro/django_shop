from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        call_command('flush', interactive=False)
        call_command('loaddata', 'categories.json', verbosity=1)
        call_command('loaddata', 'products.json', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))