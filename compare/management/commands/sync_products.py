from django.core.management.base import BaseCommand, CommandError

from compare.importers.csv_importer import import_products


class Command(BaseCommand):
    help = "Import or update RPCompare products and offers from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="products.csv",
            help="CSV file to import.",
        )

    def handle(self, *args, **options):
        filename = options["file"]

        try:
            result = import_products(filename)
        except IOError:
            raise CommandError("CSV file not found: %s" % filename)

        created, updated, offers_created, offers_updated = result

        self.stdout.write(self.style.SUCCESS(
            "Products created: %s | updated: %s | offers created: %s | offers updated: %s"
            % (created, updated, offers_created, offers_updated)
        ))
