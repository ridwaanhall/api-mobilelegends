from django.core.management.base import BaseCommand
from apps.mlbb_web.views import refresh_hero_cache, get_hero_names_dict


class Command(BaseCommand):
    help = 'Refresh hero names cache from API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--show-heroes',
            action='store_true',
            help='Display all heroes after refreshing cache',
        )

    def handle(self, *args, **options):
        self.stdout.write('Refreshing hero names cache...')
        
        success = refresh_hero_cache()
        
        if success:
            hero_dict = get_hero_names_dict()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully refreshed hero cache with {len(hero_dict)} heroes'
                )
            )
            
            if options['show_heroes']:
                self.stdout.write('\nHeroes in cache:')
                for hero_id, hero_name in sorted(hero_dict.items()):
                    self.stdout.write(f'  {hero_id}: {hero_name}')
        else:
            self.stdout.write(
                self.style.ERROR('Failed to refresh hero cache')
            )