from django.db.models import Min, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Offer, Product, Store


def home(request):
    categories = Category.objects.all().order_by("name")
    products = Product.objects.select_related("category").prefetch_related("offers__store").order_by("-updated_at")[:24]
    stores = Store.objects.filter(active=True).order_by("name")[:12]
    featured = Product.objects.select_related("category").prefetch_related(
        "offers__store"
    ).annotate(
        lowest_price=Min("offers__price")
    ).order_by("lowest_price", "-updated_at")[:12]

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "featured_products": featured,
        "stores": stores,
    })


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=cat).select_related(
        "category"
    ).prefetch_related("offers__store").annotate(
        lowest_price=Min("offers__price")
    ).order_by("name")

    return render(request, "category.html", {
        "category": cat,
        "products": products,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related(
            "offers__store", "offers__price_history"
        ),
        slug=slug,
    )
    offers = product.offers.select_related("store").filter(
        store__active=True
    ).order_by("price")
    lowest_offer = offers.first()

    return render(request, "product_detail.html", {
        "product": product,
        "offers": offers,
        "lowest_offer": lowest_offer,
    })


def search(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.none()

    if q:
        products = Product.objects.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
        ).select_related("category").prefetch_related(
            "offers__store"
        ).annotate(
            lowest_price=Min("offers__price")
        ).order_by("name")

    return render(request, "search.html", {"q": q, "products": products})


def stores(request):
    store_list = Store.objects.filter(active=True).order_by("name")
    return render(request, "stores.html", {"stores": store_list})


def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id, active=True)
    products = Product.objects.filter(
        offers__store=store
    ).distinct().select_related("category").prefetch_related(
        "offers__store"
    ).annotate(
        lowest_price=Min("offers__price")
    ).order_by("name")

    return render(request, "store_detail.html", {
        "store": store,
        "products": products,
    })


def go_to_store(request, offer_id):
    offer = get_object_or_404(
        Offer.objects.select_related("product", "store"),
        id=offer_id,
    )
    destination = offer.affiliate_url or offer.product_url

    if not destination:
        raise Http404("This offer does not have a destination URL.")

    return redirect(destination)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")
