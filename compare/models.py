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
    category = models.ForeignKey(Category, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Offer(models.Model):
    product = models.ForeignKey(Product, related_name="offers")
    store = models.ForeignKey(Store, related_name="offers")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="PKR")
    product_url = models.URLField()
    affiliate_url = models.URLField(blank=True)
    in_stock = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["price"]
    def __str__(self):
        return "%s - %s" % (self.product.name, self.store.name)

class PriceHistory(models.Model):
    offer = models.ForeignKey(
        Offer,
        related_name="price_history"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return "%s - %s" % (
            self.offer.product.name,
            self.price
        )