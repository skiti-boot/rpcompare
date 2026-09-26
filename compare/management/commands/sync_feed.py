from django.core.management.base import BaseCommand, CommandError
from compare.feed_importer import import_feed

class Command(BaseCommand):
    help = "Synchronize RPCompare products and offers from a CSV or JSON feed."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True)

    def handle(self, *args, **options):
        filename = options["file"]
        try:
            stats = import_feed(filename)
        except IOError:
            raise CommandError("Feed file not found: %s" % filename)

        self.stdout.write(self.style.SUCCESS(
            "Sync complete | products created: %s | products updated: %s | offers created: %s | offers updated: %s | prices recorded: %s | skipped: %s"
            % (stats["products_created"], stats["products_updated"],
               stats["offers_created"], stats["offers_updated"],
               stats["prices_recorded"], stats["skipped"])
        ))
