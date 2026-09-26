from django.db import models


class SyncLog(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="running")
    products_created = models.PositiveIntegerField(default=0)
    products_updated = models.PositiveIntegerField(default=0)
    offers_created = models.PositiveIntegerField(default=0)
    offers_updated = models.PositiveIntegerField(default=0)
    prices_recorded = models.PositiveIntegerField(default=0)
    skipped = models.PositiveIntegerField(default=0)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return "%s - %s" % (self.source, self.status)
