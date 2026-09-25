from django.core.management.base import BaseCommand

from compare.models import Offer


class Command(BaseCommand):

    help = "Check offers for suspicious prices and URLs"

    def handle(self, *args, **options):

        offers = Offer.objects.select_related(
            "product",
            "store"
        ).order_by(
            "product__name",
            "store__name"
        )

        for offer in offers:

            print(
                "%s | %s | Rs. %s"
                % (
                    offer.store.name,
                    offer.product.name,
                    offer.price
                )
            )

            print(
                "URL: %s"
                % offer.product_url
            )

            print("-" * 70)

        self.stdout.write(
            self.style.SUCCESS(
                "Offer check complete."
            )
        )