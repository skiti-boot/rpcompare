from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    logo = models.URLField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="offers",
        on_delete=models.CASCADE,
    )
    store = models.ForeignKey(
        Store,
        related_name="offers",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    product_url = models.URLField()
    affiliate_url = models.URLField(blank=True)
    in_stock = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price"]
        unique_together = ("product", "store")

    def __str__(self):
        return "%s - %s" % (self.product.name, self.store.name)


class PriceHistory(models.Model):
    offer = models.ForeignKey(
        Offer,
        related_name="price_history",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return "%s - %s" % (self.offer.product.name, self.price)



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
