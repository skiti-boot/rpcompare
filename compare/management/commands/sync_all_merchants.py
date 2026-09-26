from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from compare.merchant_apis.amazon_creators import import_search as amazon_import
from compare.merchant_apis.ebay_browse import import_search as ebay_import

DEFAULT_QUERIES = ['wireless headphones', 'bluetooth headphones', 'smartphone', 'android phone', 'iphone', 'laptop', 'gaming laptop', 'tablet', 'smart tv', '4k tv', 'smartwatch', 'wireless earbuds', 'gaming mouse', 'gaming keyboard', 'computer monitor', 'external hard drive', 'ssd', 'power bank', 'usb c charger', 'webcam']


class Command(BaseCommand):
    help = "Bulk-sync authorized merchant catalogs using configured API adapters."

    def add_arguments(self, parser):
        parser.add_argument("--merchant", choices=["amazon", "ebay", "both"], default="both")
        parser.add_argument(
            "--queries",
            default="",
            help="Comma-separated search queries. Defaults to the built-in catalog."
        )

    def handle(self, *args, **options):
        merchant = options["merchant"]
        raw = options.get("queries", "").strip()
        queries = [q.strip() for q in raw.split(",") if q.strip()] if raw else DEFAULT_QUERIES

        total = 0
        failures = 0

        self.stdout.write("Starting RPCompare bulk merchant sync...")
        self.stdout.write("Queries: %s" % len(queries))

        for query in queries:
            merchants = []
            if merchant in ("amazon", "both"):
                merchants.append(("amazon", amazon_import))
            if merchant in ("ebay", "both"):
                merchants.append(("ebay", ebay_import))

            for name, importer in merchants:
                self.stdout.write("Syncing %s: %s" % (name, query))
                try:
                    count = importer(query)
                    total += count
                    self.stdout.write(self.style.SUCCESS(
                        "  %s imported/updated: %s" % (name, count)
                    ))
                except Exception as exc:
                    failures += 1
                    self.stderr.write("  %s failed: %s" % (name, exc))

        self.stdout.write("")
        self.stdout.write("Bulk sync finished.")
        self.stdout.write("Products/offers imported or updated: %s" % total)
        self.stdout.write("Failed query/merchant runs: %s" % failures)

        if failures and total == 0:
            raise CommandError(
                "No merchant data was imported. Check your API credentials/access and try again."
            )
