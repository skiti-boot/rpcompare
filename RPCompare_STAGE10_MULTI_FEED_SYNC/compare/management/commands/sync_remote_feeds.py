from __future__ import print_function

import os
import tempfile
import urllib.request

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from compare.importers.csv_importer import import_products
from compare.models import SyncLog


class Command(BaseCommand):
    help = "Download and import multiple authorized merchant CSV feeds."

    def add_arguments(self, parser):
        parser.add_argument(
            "--feed",
            action="append",
            dest="feeds",
            help="Feed in the form StoreName=HTTPS_URL. Repeat for multiple feeds."
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Download timeout in seconds."
        )

    def handle(self, *args, **options):
        feeds = options.get("feeds") or []
        timeout = options.get("timeout") or 60

        # If no --feed arguments are supplied, read RPCOMPARE_FEEDS.
        # Format: Store1=https://...csv;Store2=https://...csv
        if not feeds:
            raw = os.environ.get("RPCOMPARE_FEEDS", "").strip()
            if raw:
                feeds = [item.strip() for item in raw.split(";") if item.strip()]

        if not feeds:
            raise CommandError(
                "No feeds supplied. Use --feed \"Store=URL\" or set RPCOMPARE_FEEDS."
            )

        total = {
            "products_created": 0,
            "products_updated": 0,
            "offers_created": 0,
            "offers_updated": 0,
        }
        failures = 0

        for item in feeds:
            if "=" not in item:
                self.stdout.write(self.style.ERROR(
                    "Invalid feed: %s. Use StoreName=URL" % item
                ))
                failures += 1
                continue

            name, url = item.split("=", 1)
            name = name.strip()
            url = url.strip()

            if not name or not url:
                self.stdout.write(self.style.ERROR("Invalid feed: %s" % item))
                failures += 1
                continue

            if not url.lower().startswith(("https://", "http://")):
                self.stdout.write(self.style.ERROR(
                    "%s: URL must start with http:// or https://" % name
                ))
                failures += 1
                continue

            log = SyncLog.objects.create(source=name + " | " + url, status="running")
            temp_name = None

            try:
                self.stdout.write("\n[%s] Downloading feed..." % name)
                request = urllib.request.Request(url)
                request.add_header("User-Agent", "RPCompare/1.0")
                response = urllib.request.urlopen(request, timeout=timeout)
                data = response.read()

                if not data:
                    raise RuntimeError("The feed returned no data.")

                fd, temp_name = tempfile.mkstemp(
                    prefix="rpcompare_feed_", suffix=".csv"
                )
                os.close(fd)
                with open(temp_name, "wb") as feed_file:
                    feed_file.write(data)

                self.stdout.write("[%s] Importing..." % name)
                created, updated, offers_created, offers_updated = import_products(
                    temp_name
                )

                log.products_created = created
                log.products_updated = updated
                log.offers_created = offers_created
                log.offers_updated = offers_updated
                log.status = "success"
                log.message = "Remote feed synchronization completed."
                log.finished_at = timezone.now()
                log.save()

                total["products_created"] += created
                total["products_updated"] += updated
                total["offers_created"] += offers_created
                total["offers_updated"] += offers_updated

                self.stdout.write(self.style.SUCCESS(
                    "[%s] OK | products +%s/%s | offers +%s/%s" % (
                        name, created, updated, offers_created, offers_updated
                    )
                ))

            except Exception as exc:
                failures += 1
                log.status = "failed"
                log.message = str(exc)
                log.finished_at = timezone.now()
                log.save()
                self.stdout.write(self.style.ERROR(
                    "[%s] FAILED | %s" % (name, exc)
                ))

            finally:
                if temp_name and os.path.exists(temp_name):
                    try:
                        os.remove(temp_name)
                    except OSError:
                        pass

        self.stdout.write("\nTOTAL")
        self.stdout.write(
            "Products created: %s | updated: %s | offers created: %s | offers updated: %s" % (
                total["products_created"], total["products_updated"],
                total["offers_created"], total["offers_updated"]
            )
        )

        if failures:
            raise CommandError("%s feed(s) failed." % failures)

        self.stdout.write(self.style.SUCCESS("All remote feeds completed successfully."))
