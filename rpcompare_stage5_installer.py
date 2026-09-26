from __future__ import print_function
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(ROOT, "compare", "models.py")

if not os.path.exists(models_path):
    raise SystemExit("Run this script from your RPCompare project root.")

with open(models_path, "r") as f:
    data = f.read()

if "class SyncLog(models.Model):" not in data:
    data += '''
\n\nclass SyncLog(models.Model):
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
'''
    with open(models_path, "w") as f:
        f.write(data)
    print("SyncLog added to compare/models.py")
else:
    print("SyncLog already exists")

print("Stage 5 base fix installed.")
print("Now run:")
print("python manage.py makemigrations compare")
print("python manage.py migrate")
print("python manage.py sync_feed_logged --file merchant_feed.csv")
