from django.core.management.base import BaseCommand

from animals.services.species_library import import_catalog, import_entry, import_popular, list_entries


class Command(BaseCommand):
    help = 'Import popular species into the database (from data/species_popular_ru.json)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List catalog entries without importing',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Import full catalog (not only popular species)',
        )
        parser.add_argument(
            '--library-id',
            type=str,
            help='Import one species by library id',
        )

    def handle(self, *args, **options):
        if options['list']:
            entries = list_entries(kind='catalog' if options['all'] else 'popular')
            for entry in entries:
                self.stdout.write(f"{entry['id']}: {entry['common_name']} ({entry['scientific_name']})")
            return

        library_id = options.get('library_id')
        if library_id:
            taxonomy = import_entry(library_id, kind='catalog')
            self.stdout.write(self.style.SUCCESS(f'Imported: {taxonomy.scientific_name} ({taxonomy.library_id})'))
            return

        if options['all']:
            count = import_catalog()
            self.stdout.write(self.style.SUCCESS(f'Imported {count} species from full catalog into the database'))
            return

        count = import_popular()
        self.stdout.write(self.style.SUCCESS(f'Imported {count} popular species into the database'))
