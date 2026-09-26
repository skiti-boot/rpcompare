from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compare", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SyncLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("source", models.CharField(max_length=255)),
                ("status", models.CharField(default="running", max_length=20)),
                ("products_created", models.PositiveIntegerField(default=0)),
                ("products_updated", models.PositiveIntegerField(default=0)),
                ("offers_created", models.PositiveIntegerField(default=0)),
                ("offers_updated", models.PositiveIntegerField(default=0)),
                ("prices_recorded", models.PositiveIntegerField(default=0)),
                ("skipped", models.PositiveIntegerField(default=0)),
                ("message", models.TextField(blank=True)),
            ],
            options={"ordering": ["-started_at"]},
        ),
    ]
