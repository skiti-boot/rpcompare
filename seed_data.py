from compare.models import Category, Store, Product, Offer


# --------------------------------------------------
# CATEGORIES
# --------------------------------------------------

categories = {}

category_data = [
    ("Smartphones", "smartphones"),
    ("Laptops", "laptops"),
    ("Headphones", "headphones"),
    ("TVs", "tvs"),
    ("Smartwatches", "smartwatches"),
    ("Accessories", "accessories"),
]

for name, slug in category_data:
    category, created = Category.objects.get_or_create(
        slug=slug,
        defaults={"name": name}
    )
    categories[name] = category


# --------------------------------------------------
# STORES
# --------------------------------------------------

store_data = [
    ("Daraz", "https://www.daraz.pk/"),
    ("PriceOye", "https://priceoye.pk/"),
    ("Shophive", "https://www.shophive.com/"),
    ("Telemart", "https://www.telemart.pk/"),
    ("Mega.pk", "https://www.mega.pk/"),
    ("iShopping", "https://www.ishopping.pk/"),
]

stores = {}

for name, website in store_data:
    store, created = Store.objects.get_or_create(
        name=name,
        defaults={"website": website}
    )
    stores[name] = store


# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

products = [
    {
        "name": "Samsung Galaxy S26",
        "slug": "samsung-galaxy-s26",
        "category": "Smartphones",
        "description": "Samsung Galaxy S26 smartphone.",
    },
    {
        "name": "Apple iPhone 17",
        "slug": "apple-iphone-17",
        "category": "Smartphones",
        "description": "Apple iPhone 17 smartphone.",
    },
    {
        "name": "Sony WH-1000XM5",
        "slug": "sony-wh-1000xm5",
        "category": "Headphones",
        "description": "Sony WH-1000XM5 wireless noise-cancelling headphones.",
    },
    {
        "name": "Samsung 55Q6F 55 Inch TV",
        "slug": "samsung-55q6f-55-inch-tv",
        "category": "TVs",
        "description": "Samsung 55Q6F 55 inch 4K QLED television.",
    },
    {
        "name": "Lenovo IdeaPad Slim 3",
        "slug": "lenovo-ideapad-slim-3",
        "category": "Laptops",
        "description": "Lenovo IdeaPad Slim 3 laptop.",
    },
]


# --------------------------------------------------
# VERIFIED PRODUCT OFFERS
# --------------------------------------------------

offers = {

    "samsung-galaxy-s26": [
        (
            "Daraz",
            319998,
            "https://www.daraz.pk/products/samsung-galaxy-s26-256-gb-i1948100119.html"
        ),
        (
            "PriceOye",
            284500,
            "https://priceoye.pk/mobiles/samsung/samsung-galaxy-s26"
        ),
        (
            "Shophive",
            329999,
            "https://www.shophive.com/samsung-galaxy-s26-12gb-512gb/"
        ),
    ],

    "apple-iphone-17": [
        (
            "Daraz",
            399000,
            "https://www.daraz.pk/products/apple-iphone-17-256-gb-i1957775261.html"
        ),
        (
            "PriceOye",
            354999,
            "https://priceoye.pk/mobiles/apple/apple-iphone-17/%7B%7BprodcutUrl%7D%7D"
        ),
    ],

    "sony-wh-1000xm5": [
        (
            "PriceOye",
            73999,
            "https://priceoye.pk/wireless-earbuds/sony/sony-wh-1000xm5-wireless-anc-headphones/ppc/silver"
        ),
        (
            "Shophive",
            76499,
            "https://www.shophive.com/sony-wh-1000xm5-wireless-noise-canceling-headphones/"
        ),
    ],

    "samsung-55q6f-55-inch-tv": [
        (
            "Shophive",
            168999,
            "https://www.shophive.com/samsung-55q6f-55-4k-suhd-flat-qled-tv/"
        ),
    ],

    "lenovo-ideapad-slim-3": [
        (
            "PriceOye",
            177999,
            "https://priceoye.pk/laptops/lenovo"
        ),
    ],
}


# --------------------------------------------------
# CREATE / UPDATE PRODUCTS
# --------------------------------------------------

for item in products:

    product, created = Product.objects.update_or_create(
        slug=item["slug"],
        defaults={
            "name": item["name"],
            "category": categories[item["category"]],
            "description": item["description"],
        }
    )

    # Remove old incorrect offers.
    product.offers.all().delete()

    # Add verified offers.
    for store_name, price, product_url in offers.get(item["slug"], []):

        Offer.objects.create(
            product=product,
            store=stores[store_name],
            price=price,
            currency="PKR",
            product_url=product_url,
            in_stock=True
        )


# --------------------------------------------------
# REMOVE OLD EMPTY ELECTRONICS CATEGORY
# --------------------------------------------------

try:
    old_category = Category.objects.get(slug="electronics")

    if old_category.products.count() == 0:
        old_category.delete()

except Category.DoesNotExist:
    pass


print("RPcompare categories, products and offers updated successfully!")