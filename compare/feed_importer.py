import csv
import json
import os
from django.utils.text import slugify
from .models import Category, Store, Product, Offer, PriceHistory

def _clean(value):
    return "" if value is None else str(value).strip()

def _bool(value, default=True):
    value = _clean(value).lower()
    if not value:
        return default
    return value not in ("0", "false", "no", "out", "unavailable")

def _row(row):
    return {k: _clean(row.get(k)) for k in ("category","store","store_website","store_logo","name","slug","description","image_url","price","currency","product_url","affiliate_url")}

def import_rows(rows):
    stats={"products_created":0,"products_updated":0,"offers_created":0,"offers_updated":0,"prices_recorded":0,"skipped":0}
    for raw in rows:
        row=_row(raw)
        row["currency"]=row["currency"] or "USD"
        row["in_stock"]=_bool(raw.get("in_stock"),True)
        if not row["category"] or not row["store"] or not row["name"]:
            stats["skipped"]+=1; continue
        category,_=Category.objects.get_or_create(slug=slugify(row["category"]),defaults={"name":row["category"]})
        store,_=Store.objects.get_or_create(name=row["store"],defaults={"website":row["store_website"],"logo":row["store_logo"]})
        changed=False
        if row["store_website"] and not store.website: store.website=row["store_website"]; changed=True
        if row["store_logo"] and not store.logo: store.logo=row["store_logo"]; changed=True
        if changed: store.save()
        product,created=Product.objects.update_or_create(slug=row["slug"] or slugify(row["name"]),defaults={"name":row["name"],"description":row["description"],"image_url":row["image_url"],"category":category})
        stats["products_created" if created else "products_updated"]+=1
        if not row["price"] or not row["product_url"]: continue
        existing=Offer.objects.filter(product=product,store=store).first()
        old_price=existing.price if existing else None
        offer,offer_created=Offer.objects.update_or_create(product=product,store=store,defaults={"price":row["price"],"currency":row["currency"],"product_url":row["product_url"],"affiliate_url":row["affiliate_url"],"in_stock":row["in_stock"]})
        stats["offers_created" if offer_created else "offers_updated"]+=1
        if offer_created or old_price != offer.price:
            PriceHistory.objects.create(offer=offer,price=offer.price); stats["prices_recorded"]+=1
    return stats

def import_csv(filename):
    with open(filename,"r") as handle: return import_rows(csv.DictReader(handle))

def import_json(filename):
    with open(filename,"r") as handle: data=json.load(handle)
    if isinstance(data,dict): data=data.get("products",data.get("items",[]))
    return import_rows(data)

def import_feed(filename):
    return import_json(filename) if os.path.splitext(filename)[1].lower()==".json" else import_csv(filename)
