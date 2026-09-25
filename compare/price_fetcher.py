import json
import re
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/109.0 Safari/537.36"
)


def clean_price(value):
    if value is None:
        return None

    value = str(value)

    value = value.replace(",", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace("PKR", "")
    value = value.strip()

    match = re.search(r"\d+(?:\.\d+)?", value)

    if not match:
        return None

    try:
        price = Decimal(match.group())
    except InvalidOperation:
        return None

    # Reject obviously invalid prices.
    if price <= 0:
        return None

    return price


def download_page(url):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def find_json_ld_price(soup):
    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:
            data = json.loads(
                script.string or script.get_text()
            )
        except Exception:
            continue

        objects = data if isinstance(data, list) else [data]

        for obj in objects:

            if not isinstance(obj, dict):
                continue

            offers = obj.get("offers")

            if isinstance(offers, dict):

                price = clean_price(
                    offers.get("price")
                )

                if price:
                    return price

            if isinstance(offers, list):

                for offer in offers:

                    if not isinstance(offer, dict):
                        continue

                    price = clean_price(
                        offer.get("price")
                    )

                    if price:
                        return price

            if obj.get("@type") == "Offer":

                price = clean_price(
                    obj.get("price")
                )

                if price:
                    return price

    return None


def find_meta_price(soup):
    selectors = [
        ('meta[itemprop="price"]', "content"),
        ('meta[property="product:price:amount"]', "content"),
    ]

    for selector, attribute in selectors:

        element = soup.select_one(selector)

        if element:

            price = clean_price(
                element.get(attribute)
            )

            if price:
                return price

    return None


def find_store_price(soup, url):
    url = url.lower()

    # Do NOT use broad [class*='price'] selectors.
    # They can capture shipping, installments,
    # discounts, product IDs, etc.

    if "daraz.pk" in url:

        selectors = [
            ".pdp-product-price",
            ".pdp-price",
        ]

    elif "priceoye.pk" in url:

        selectors = [
            ".product-price",
            ".price-box",
            ".price",
        ]

    elif "shophive.com" in url:

        selectors = [
            ".price-box .price",
            ".special-price .price",
            ".product-info-price .price",
            ".price-wrapper .price",
        ]

    elif "telemart.pk" in url:

        selectors = [
            ".price",
            ".product-price",
            ".special-price",
        ]

    elif "mega.pk" in url:

        selectors = [
            ".price",
            ".product-price",
        ]

    else:

        selectors = [
            '[itemprop="price"]',
            ".product-price",
            ".sale-price",
            ".special-price",
            ".current-price",
        ]

    for selector in selectors:

        elements = soup.select(selector)

        for element in elements:

            price = clean_price(
                element.get_text(
                    " ",
                    strip=True
                )
            )

            if price:
                return price

    return None


def fetch_price(url):

    html = download_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # 1. Structured product data.
    price = find_json_ld_price(soup)

    if price:
        return price

    # 2. Standard price metadata.
    price = find_meta_price(soup)

    if price:
        return price

    # 3. Store-specific HTML.
    price = find_store_price(
        soup,
        url
    )

    return price