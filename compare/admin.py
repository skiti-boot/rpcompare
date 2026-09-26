from django.contrib import admin
from .models import Category, Store, Product, Offer, PriceHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "website")
    list_filter = ("active",)
    search_fields = ("name",)
    list_editable = ("active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "updated_at")
    list_filter = ("category",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("product", "store", "price", "currency", "in_stock", "updated_at")
    list_filter = ("store", "currency", "in_stock")
    search_fields = ("product__name", "store__name")
    list_editable = ("price", "in_stock")


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("offer", "price", "recorded_at")
    list_filter = ("recorded_at",)
