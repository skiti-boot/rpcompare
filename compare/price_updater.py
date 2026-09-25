from django.db import transaction

from .models import Offer, PriceHistory
from .price_fetcher import fetch_price


def suspicious_price(offer, new_price):

    old_price = offer.price

    if not old_price:
        return False

    difference = abs(
        new_price - old_price
    )

    percentage = (
        difference / old_price
    ) * 100

    if percentage > 50:
        return True

    if new_price < 500:
        return True

    return False


def update_offer(offer):

    print(
        "Checking: %s | %s"
        % (
            offer.store.name,
            offer.product.name
        )
    )

    try:

        price = fetch_price(
            offer.product_url
        )

    except Exception as error:

        print(
            "ERROR: %s"
            % error
        )

        return False


    if price is None:

        print(
            "PRICE NOT FOUND: %s"
            % offer.product.name
        )

        return False


    if suspicious_price(
        offer,
        price
    ):

        print(
            "SUSPICIOUS PRICE: %s -> %s"
            % (
                offer.price,
                price
            )
        )

        print(
            "Price was NOT changed."
        )

        return False


    old_price = offer.price


    with transaction.atomic():

        if old_price != price:

            offer.price = price

            offer.save(
                update_fields=[
                    "price",
                    "updated_at"
                ]
            )

            PriceHistory.objects.create(
                offer=offer,
                price=price
            )

            print(
                "PRICE CHANGED: %s -> %s"
                % (
                    old_price,
                    price
                )
            )

            return True


        if not offer.price_history.exists():

            PriceHistory.objects.create(
                offer=offer,
                price=price
            )

            print(
                "INITIAL PRICE HISTORY: %s"
                % price
            )

            return True


    print(
        "PRICE UNCHANGED: %s"
        % price
    )

    return False


def update_all_offers():

    offers = Offer.objects.select_related(
        "product",
        "store"
    ).filter(
        in_stock=True
    ).exclude(
        product_url=""
    )

    updated = 0

    checked = 0

    for offer in offers:

        checked += 1

        if update_offer(offer):
            updated += 1


    print(
        "Finished. Checked: %s | Updated: %s"
        % (
            checked,
            updated
        )
    )

    return updated