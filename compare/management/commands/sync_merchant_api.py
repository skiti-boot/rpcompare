from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Import live catalog data from an authorized merchant API."

    def add_arguments(self, parser):
        parser.add_argument("--merchant", choices=["amazon", "ebay"], required=True)
        parser.add_argument("--query", required=True)

    def handle(self, *args, **options):
        try:
            if options["merchant"] == "amazon":
                from compare.merchant_apis.amazon_creators import import_search
            else:
                from compare.merchant_apis.ebay_browse import import_search
            count = import_search(options["query"])
        except Exception as exc:
            raise CommandError(str(exc))
        self.stdout.write(self.style.SUCCESS(
            "%s live offers imported: %s" % (options["merchant"], count)
        ))
