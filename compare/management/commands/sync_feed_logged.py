from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from compare.feed_importer import import_feed
from compare.models import SyncLog

class Command(BaseCommand):
    help = "Synchronize a feed and record the result."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True)

    def handle(self, *args, **options):
        filename = options["file"]
        log = SyncLog.objects.create(source=filename, status="running")
        try:
            stats = import_feed(filename)
            for key in ("products_created", "products_updated",
                        "offers_created", "offers_updated",
                        "prices_recorded", "skipped"):
                setattr(log, key, stats.get(key, 0))
            log.status = "success"
            log.message = "Feed synchronization completed successfully."
            log.finished_at = timezone.now()
            log.save()
            self.stdout.write(self.style.SUCCESS(
                "Sync complete | products +%s/%s | offers +%s/%s | prices %s | skipped %s"
                % (log.products_created, log.products_updated,
                   log.offers_created, log.offers_updated,
                   log.prices_recorded, log.skipped)
            ))
        except Exception as exc:
            log.status = "failed"
            log.message = str(exc)
            log.finished_at = timezone.now()
            log.save()
            raise CommandError("Feed synchronization failed: %s" % exc)
