import csv

from django.utils.text import slugify

from compare.models import Category, Store, Product, Offer, PriceHistory


def import_products(filename):
    created = 0
    updated = 0
    offers_created = 0
    offers_updated = 0

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            category_name = row.get("category", "").strip()
            store_name = row.get("store", "").strip()
            name = row.get("name", "").strip()
            slug = row.get("slug", "").strip() or slugify(name)

            if not category_name or not store_name or not name or not slug:
                continue

            category, _ = Category.objects.get_or_create(
                slug=slugify(category_name),
                defaults={"name": category_name},
            )

            store, _ = Store.objects.get_or_create(
                name=store_name,
                defaults={
                    "website": row.get("store_website", "").strip(),
                },
            )

            product, product_created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": row.get("description", "").strip(),
                    "image_url": row.get("image_url", "").strip(),
                    "category": category,
                },
            )

            if product_created:
                created += 1
            else:
                updated += 1

            price = row.get("price", "").strip()
            product_url = row.get("product_url", "").strip()

            if not price or not product_url:
                continue

            affiliate_url = row.get("affiliate_url", "").strip()
            currency = row.get("currency", "USD").strip() or "USD"
            in_stock = row.get(
                "in_stock", "true"
            ).strip().lower() not in ("0", "false", "no", "out")

            offer = Offer.objects.filter(
                product=product,
                store=store,
            ).first()

            old_price = offer.price if offer else None

            offer, offer_created = Offer.objects.update_or_create(
                product=product,
                store=store,
                defaults={
                    "price": price,
                    "currency": currency,
                    "product_url": product_url,
                    "affiliate_url": affiliate_url,
                    "in_stock": in_stock,
                },
            )

            if offer_created:
                offers_created += 1
                PriceHistory.objects.create(
                    offer=offer,
                    price=offer.price,
                )
            else:
                offers_updated += 1
                if old_price is None or old_price != offer.price:
                    PriceHistory.objects.create(
                        offer=offer,
                        price=offer.price,
                    )

    return created, updated, offers_created, offers_updated
