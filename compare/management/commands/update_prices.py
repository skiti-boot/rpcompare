from django.core.management.base import BaseCommand

from compare.price_updater import update_all_offers


class Command(BaseCommand):

    help = "Update product prices from online stores"

    def handle(self, *args, **options):

        self.stdout.write(
            "Updating product prices..."
        )

        updated = update_all_offers()

        self.stdout.write(
            self.style.SUCCESS(
                "Finished. %s prices actually updated."
                % updated
            )
        )