from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch

from .models import Product, Category, Offer, Store


def available_offers():
    return Offer.objects.filter(
        in_stock=True
    ).select_related(
        "store"
    ).order_by("price")


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    stores = Store.objects.all()

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "stores": stores,
    })
    


def search(request):

    q = request.GET.get("q", "").strip()

    if q:

        products = Product.objects.filter(
            offers__in_stock=True
        ).filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).distinct().prefetch_related(
            Prefetch(
                "offers",
                queryset=available_offers(),
                to_attr="available_offers"
            )
        )

    else:

        products = Product.objects.none()

    return render(
        request,
        "search.html",
        {
            "products": products,
            "q": q,
        }
    )


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    offers = list(
        product.offers.filter(
            in_stock=True
        ).select_related(
            "store"
        ).prefetch_related(
            "price_history"
        ).order_by("price")
    )

    for offer in offers:

        history = list(
            offer.price_history.all()[:2]
        )

        offer.previous_price = None
        offer.price_drop = None
        offer.price_drop_percent = None

        if len(history) >= 2:

            current = history[0].price
            previous = history[1].price

            if previous > current:

                offer.previous_price = previous

                offer.price_drop = (
                    previous - current
                )

                offer.price_drop_percent = (
                    (previous - current)
                    / previous
                ) * 100

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "offers": offers,
        }
    )


def category(request, slug):

    category_obj = get_object_or_404(
        Category,
        slug=slug
    )

    categories = Category.objects.exclude(
        slug="electronics"
    ).order_by("name")

    products = category_obj.products.filter(
        offers__in_stock=True
    ).distinct().order_by(
        "-updated_at"
    ).prefetch_related(
        Prefetch(
            "offers",
            queryset=available_offers(),
            to_attr="available_offers"
        )
    )

    return render(
        request,
        "category.html",
        {
            "category": category_obj,
            "products": products,
            "categories": categories,
        }
    )


def about(request):

    return render(
        request,
        "simple.html",
        {
            "title": "About RPcompare",
            "text": (
                "RPcompare makes it easier to compare "
                "electronics prices from different online stores."
            )
        }
    )


def contact(request):

    return render(
        request,
        "simple.html",
        {
            "title": "Contact",
            "text": (
                "For questions, partnerships, or corrections, "
                "contact the RPcompare team."
            )
        }
    )


def privacy(request):

    return render(
        request,
        "simple.html",
        {
            "title": "Privacy Policy",
            "text": (
                "This page will contain RPcompare's privacy "
                "policy before public launch."
            )
        }
    )


def terms(request):

    return render(
        request,
        "simple.html",
        {
            "title": "Terms of Use",
            "text": (
                "This page will contain RPcompare's terms "
                "of use before public launch."
            )
        }
    )


def go_to_offer(request, offer_id):

    offer = get_object_or_404(
        Offer,
        id=offer_id
    )

    url = offer.affiliate_url or offer.product_url

    return redirect(url)

def stores(request):
    stores = Store.objects.all().order_by("name")

    return render(
        request,
        "stores.html",
        {
            "stores": stores,
        }
    )

def store_detail(request, store_id):
    store = Store.objects.get(id=store_id)

    offers = Offer.objects.filter(
        store=store
    ).select_related(
        "product"
    )

    products = []

    for offer in offers:
        products.append(offer.product)

    return render(
        request,
        "store_detail.html",
        {
            "store": store,
            "products": products,
        }
    )