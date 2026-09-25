from django.contrib import admin

from .models import (
    Category,
    Store,
    Product,
    Offer,
    PriceHistory
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
        "slug",
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "website",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "website",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "updated_at",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "store",
        "price",
        "currency",
        "in_stock",
        "updated_at",
    )

    list_filter = (
        "store",
        "in_stock",
        "currency",
    )

    search_fields = (
        "product__name",
        "store__name",
        "product_url",
    )

    list_editable = (
        "price",
        "in_stock",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "product__name",
        "price",
    )


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "offer",
        "price",
        "recorded_at",
    )

    list_filter = (
        "offer__store",
    )

    search_fields = (
        "offer__product__name",
        "offer__store__name",
    )

    readonly_fields = (
        "offer",
        "price",
        "recorded_at",
    )

    ordering = (
        "-recorded_at",
    )