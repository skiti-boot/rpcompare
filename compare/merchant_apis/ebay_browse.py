from __future__ import print_function

import base64
import json
import os
import urllib.request
import urllib.parse

from django.utils.text import slugify
from compare.models import Category, Store, Product, Offer, PriceHistory


def _get(url, headers):
    request = urllib.request.Request(url)
    for key, value in headers.items():
        request.add_header(key, value)

    response = urllib.request.urlopen(request, timeout=30)
    return json.loads(response.read().decode("utf-8"))


def _token():
    client_id = os.environ.get("EBAY_CLIENT_ID")
    client_secret = os.environ.get("EBAY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "eBay credentials are not configured. "
            "Set EBAY_CLIENT_ID and EBAY_CLIENT_SECRET first."
        )

    raw = (
        client_id + ":" + client_secret
    ).encode("utf-8")

    auth = base64.b64encode(raw).decode("ascii")

    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.ebay.com/identity/v1/oauth2/token",
        data=body
    )

    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )
    request.add_header(
        "Authorization",
        "Basic " + auth
    )

    response = urllib.request.urlopen(request, timeout=30)
    result = json.loads(response.read().decode("utf-8"))

    if "access_token" not in result:
        raise RuntimeError("eBay did not return an access token.")

    return result["access_token"]


def import_search(keywords):
    params = urllib.parse.urlencode({
        "q": keywords,
        "limit": "100",
    })

    headers = {
        "Authorization": "Bearer " + _token(),
        "X-EBAY-C-MARKETPLACE-ID": os.environ.get(
            "EBAY_MARKETPLACE_ID",
            "EBAY_US"
        ),
        "Accept": "application/json",
    }

    campaign = os.environ.get("EBAY_CAMPAIGN_ID")

    if campaign:
        headers["X-EBAY-C-ENDUSERCTX"] = (
            "affiliateCampaignId=%s,affiliateReferenceId=%s"
            % (
                campaign,
                os.environ.get(
                    "EBAY_REFERENCE_ID",
                    "rpcompare"
                ),
            )
        )

    url = (
        "https://api.ebay.com/"
        "buy/browse/v1/item_summary/search?"
        + params
    )

    data = _get(url, headers)

    store, _ = Store.objects.get_or_create(
        name="eBay",
        defaults={
            "website": "https://www.ebay.com",
            "active": True,
        }
    )

    category, _ = Category.objects.get_or_create(
        slug="electronics",
        defaults={"name": "Electronics"},
    )

    count = 0

    for item in data.get("itemSummaries", []):
        title = item.get("title")
        item_id = item.get("itemId")
        price = item.get("price", {}).get("value")

        if not title or not item_id or price is None:
            continue

        affiliate_url = (
            item.get("itemAffiliateWebUrl")
            or item.get("itemWebUrl")
        )

        if not affiliate_url:
            continue

        product, _ = Product.objects.update_or_create(
            slug=(
                slugify(title)[:50]
                + "-"
                + slugify(item_id)[-20:]
            ),
            defaults={
                "name": title,
                "category": category,
                "description": title,
                "image_url": item.get(
                    "image",
                    {}
                ).get(
                    "imageUrl",
                    ""
                ),
            }
        )

        offer, _ = Offer.objects.update_or_create(
            product=product,
            store=store,
            defaults={
                "price": price,
                "currency": item.get(
                    "price",
                    {}
                ).get(
                    "currency",
                    "USD"
                ),
                "product_url": item.get(
                    "itemWebUrl",
                    affiliate_url
                ),
                "affiliate_url": affiliate_url,
                "in_stock": True,
            }
        )

        PriceHistory.objects.create(
            offer=offer,
            price=offer.price
        )

        count += 1

    return count
