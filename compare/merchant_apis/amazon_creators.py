from __future__ import print_function

import json
import os
import urllib.request
import urllib.parse

from django.utils.text import slugify
from compare.models import Category, Store, Product, Offer, PriceHistory


def _post(url, payload, headers=None):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    request.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    response = urllib.request.urlopen(request, timeout=30)
    return json.loads(response.read().decode("utf-8"))


def _token():
    client_id = os.environ.get("AMAZON_CREATOR_CLIENT_ID")
    client_secret = os.environ.get("AMAZON_CREATOR_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Amazon credentials are not configured. Set AMAZON_CREATOR_CLIENT_ID "
            "and AMAZON_CREATOR_CLIENT_SECRET first."
        )

    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "creatorsapi::default",
    }).encode("utf-8")

    request = urllib.request.Request(
        os.environ.get(
            "AMAZON_CREATOR_TOKEN_URL",
            "https://api.amazon.com/auth/o2/token"
        ),
        data=body
    )
    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

    response = urllib.request.urlopen(request, timeout=30)
    result = json.loads(response.read().decode("utf-8"))

    if "access_token" not in result:
        raise RuntimeError("Amazon did not return an access token.")

    return result["access_token"]


def import_search(keywords):
    marketplace = os.environ.get(
        "AMAZON_MARKETPLACE",
        "www.amazon.com"
    )
    partner_tag = os.environ.get("AMAZON_PARTNER_TAG")

    if not partner_tag:
        raise RuntimeError(
            "Amazon partner tag is not configured. "
            "Set AMAZON_PARTNER_TAG first."
        )

    payload = {
        "keywords": keywords,
        "marketplace": marketplace,
        "partnerTag": partner_tag,
        "resources": [
            "images.primary.large",
            "itemInfo.title",
            "offersV2.listings",
        ],
    }

    data = _post(
        "https://creatorsapi.amazon/catalog/v1/searchItems",
        payload,
        {
            "Authorization": "Bearer " + _token(),
            "x-marketplace": marketplace,
        }
    )

    store, _ = Store.objects.get_or_create(
        name="Amazon",
        defaults={
            "website": "https://www.amazon.com",
            "active": True,
        }
    )

    category, _ = Category.objects.get_or_create(
        slug="electronics",
        defaults={"name": "Electronics"},
    )

    count = 0

    for item in data.get("searchResult", {}).get("items", []):
        asin = item.get("asin")
        title = (
            item.get("itemInfo", {})
            .get("title", {})
            .get("displayValue")
        )

        if not asin or not title:
            continue

        product, _ = Product.objects.update_or_create(
            slug=slugify(title)[:50] + "-" + asin.lower(),
            defaults={
                "name": title,
                "category": category,
                "description": title,
                "image_url": (
                    item.get("images", {})
                    .get("primary", {})
                    .get("large", {})
                    .get("url", "")
                ),
            }
        )

        listings = (
            item.get("offersV2", {})
            .get("listings", [])
        )

        if not listings:
            continue

        money = listings[0].get("price", {}).get("money", {})
        price = money.get("amount")
        url = (
            item.get("detailPageURL")
            or item.get("detailPageUrl")
        )

        if price is None or not url:
            continue

        offer, _ = Offer.objects.update_or_create(
            product=product,
            store=store,
            defaults={
                "price": price,
                "currency": money.get(
                    "currencyCode",
                    "USD"
                ),
                "product_url": url,
                "affiliate_url": url,
                "in_stock": True,
            }
        )

        PriceHistory.objects.create(
            offer=offer,
            price=offer.price
        )

        count += 1

    return count
