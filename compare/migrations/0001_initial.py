from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("website", models.URLField(blank=True)),
                ("logo", models.URLField(blank=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True)),
                ("image_url", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="compare.Category")),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="USD", max_length=10)),
                ("product_url", models.URLField()),
                ("affiliate_url", models.URLField(blank=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="compare.Product")),
                ("store", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="compare.Store")),
            ],
            options={"ordering": ["price"], "unique_together": {("product", "store")}},
        ),
        migrations.CreateModel(
            name="PriceHistory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("recorded_at", models.DateTimeField(auto_now_add=True)),
                ("offer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="price_history", to="compare.Offer")),
            ],
            options={"ordering": ["-recorded_at"]},
        ),
    ]
