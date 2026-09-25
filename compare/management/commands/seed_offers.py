from django.core.management.base import BaseCommand

from compare.models import Product, Store, Offer


OFFERS = [

    (
        "Samsung Galaxy S25",
        "PriceOye",
        269999,
        "https://priceoye.pk/mobiles/samsung/samsung-galaxy-s25"
    ),

    (
        "Samsung Galaxy S25",
        "Daraz",
        349899,
        "https://www.daraz.pk/products/samsung-galaxy-s25-5g-12gb-ram-512gb-rom-snapdragon-8-elite-50mp-triple-camera-62-dynamic-amoled-120hz-gorilla-glass-victus-2-ip68-android-15-4000mah-battery-i721773998.html"
    ),

    (
        "Sony WH-1000XM5",
        "PriceOye",
        73999,
        "https://priceoye.pk/wireless-earbuds/compare/sony-wh-1000xm5-wireless-anc-headphones"
    ),

    (
        "Sony WH-1000XM5",
        "Shophive",
        76499,
        "https://www.shophive.com/sony-wh-1000xm5-wireless-noise-canceling-headphones/"
    ),

    (
        "Lenovo IdeaPad Slim 3",
        "PriceOye",
        177999,
        "https://priceoye.pk/laptops/lenovo/lenovo-ideapad-slim-3-core-i5-13th-gen-8gb-512gb"
    ),

    (
        "Lenovo IdeaPad Slim 3",
        "Shophive",
        260999,
        "https://www.shophive.com/lenovo-ideapad-slim-3-15amn8-amd-ryzen-5-40-16gb-ram-512gb-ssd-laptop-1-year-warranty/"
    ),

    (
        "Samsung Galaxy A36 5G",
        "PriceOye",
        104999,
        "https://priceoye.pk/mobiles/samsung/samsung-galaxy-a36-5g"
    ),

    (
        "Apple AirPods Pro",
        "PriceOye",
        57999,
        "https://priceoye.pk/wireless-earbuds/apple/apple-airpods-pro/1000"
    ),

    (
        "Samsung Galaxy Watch 7",
        "Daraz",
        52999,
        "https://www.daraz.pk/products/samsung-galaxy-watch-7-44mm-sm-l310-i531518326.html"
    ),
]


class Command(BaseCommand):

    help = "Add verified store offers"

    def handle(self, *args, **options):

        added = 0
        updated = 0

        for product_name, store_name, price, url in OFFERS:

            try:
                product = Product.objects.get(
                    name=product_name
                )
            except Product.DoesNotExist:

                self.stdout.write(
                    "SKIPPED - product not found: %s"
                    % product_name
                )

                continue

            store, created = Store.objects.get_or_create(
                name=store_name,
                defaults={
                    "website": url,
                    "active": True
                }
            )

            offer, created = Offer.objects.get_or_create(
                product=product,
                store=store,
                defaults={
                    "price": price,
                    "currency": "PKR",
                    "product_url": url,
                    "in_stock": True
                }
            )

            if created:

                added += 1

                self.stdout.write(
                    "ADDED: %s | %s"
                    % (
                        product_name,
                        store_name
                    )
                )

            else:

                offer.price = price
                offer.product_url = url
                offer.in_stock = True

                offer.save(
                    update_fields=[
                        "price",
                        "product_url",
                        "in_stock"
                    ]
                )

                updated += 1

                self.stdout.write(
                    "UPDATED: %s | %s"
                    % (
                        product_name,
                        store_name
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "DONE - Added: %s | Updated: %s"
                % (
                    added,
                    updated
                )
            )
        )