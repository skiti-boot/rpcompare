from django.core.management.base import BaseCommand

from compare.models import Product, Store, Offer


OFFERS = [

    # IPHONE 17
    (
        "Apple iPhone 17",
        "Daraz",
        399000,
        "https://www.daraz.pk/products/apple-iphone-17-256-gb-i1957775261.html"
    ),

    (
        "Apple iPhone 17",
        "PriceOye",
        354999,
        "https://priceoye.pk/mobiles/apple/apple-iphone-17"
    ),


    # SAMSUNG GALAXY S26
    (
        "Samsung Galaxy S26",
        "Daraz",
        319998,
        "https://www.daraz.pk/products/samsung-galaxy-s26-256-gb-i1948100119.html"
    ),

    (
        "Samsung Galaxy S26",
        "PriceOye",
        284500,
        "https://priceoye.pk/mobiles/samsung/samsung-galaxy-s26"
    ),

    (
        "Samsung Galaxy S26",
        "Shophive",
        329999,
        "https://www.shophive.com/samsung-galaxy-s26-12gb-512gb/"
    ),


    # SONY HEADPHONES
    (
        "Sony WH-1000XM5",
        "PriceOye",
        73999,
        "https://priceoye.pk/wireless-earbuds/sony/sony-wh-1000xm5-wireless-anc-headphones/ppc/silver"
    ),

    (
        "Sony WH-1000XM5",
        "Shophive",
        76499,
        "https://www.shophive.com/sony-wh-1000xm5-wireless-noise-canceling-headphones/"
    ),


    # SAMSUNG TV
    (
        "Samsung 55Q6F 55 Inch TV",
        "Shophive",
        168999,
        "https://www.shophive.com/samsung-55q6f-55-4k-suhd-flat-qled-tv/"
    ),


    # IPHONE 15
    (
        "iPhone 15",
        "PriceOye",
        264999,
        "https://priceoye.pk/mobiles/apple/apple-iphone-15"
    ),
]


class Command(BaseCommand):

    help = "Restore valid multi-store product offers"

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
                    "PRODUCT NOT FOUND: %s"
                    % product_name
                )

                continue


            try:
                store = Store.objects.get(
                    name=store_name
                )
            except Store.DoesNotExist:

                store = Store.objects.create(
                    name=store_name,
                    active=True
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
                "DONE — Added: %s | Updated: %s"
                % (
                    added,
                    updated
                )
            )
        )