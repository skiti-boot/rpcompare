from django.contrib import admin

from .models import SyncLog


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = (
        "source", "status", "started_at", "finished_at",
        "products_created", "products_updated",
        "offers_created", "offers_updated",
        "prices_recorded", "skipped",
    )
    list_filter = ("status",)
    search_fields = ("source", "message")
    readonly_fields = ("started_at", "finished_at")
