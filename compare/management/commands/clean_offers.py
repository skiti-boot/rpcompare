from django.core.management.base import BaseCommand

from compare.models import Offer


class Command(BaseCommand):

    help = "Disable offers that use store homepages or invalid URLs"

    def handle(self, *args, **options):

        bad_urls = [
            "https://www.daraz.pk/",
            "https://www.mega.pk/",
            "https://priceoye.pk/",
            "https://www.shophive.com/",
            "https://www.telemart.pk/",
            "https://www.ishopping.pk/",
            "https://priceoye.pk/laptops/lenovo",
        ]

        count = 0

        for offer in Offer.objects.all():

            url = offer.product_url.strip()

            if url in bad_urls or "{{" in url or "%7B%7B" in url:

                offer.in_stock = False

                offer.save(
                    update_fields=["in_stock"]
                )

                print(
                    "DISABLED: %s | %s"
                    % (
                        offer.store.name,
                        offer.product.name
                    )
                )

                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Disabled %s invalid offers."
                % count
            )
        )