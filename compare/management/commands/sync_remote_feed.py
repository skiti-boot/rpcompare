from __future__ import print_function

import os
import tempfile
import urllib.request

from django.core.management.base import BaseCommand, CommandError
from compare.importers.csv_importer import import_products


class Command(BaseCommand):
    help = "Download an authorized merchant CSV feed and import it into RPCompare."

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            help="HTTPS/HTTP URL of an authorized CSV product feed."
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Download timeout in seconds."
        )

    def handle(self, *args, **options):
        url = options["url"]
        timeout = options["timeout"]

        if not url.lower().startswith(("https://", "http://")):
            raise CommandError("Feed URL must start with http:// or https://")

        temp_name = None
        try:
            self.stdout.write("Downloading feed...")
            request = urllib.request.Request(url)
            request.add_header("User-Agent", "RPCompare/1.0")
            response = urllib.request.urlopen(request, timeout=timeout)
            data = response.read()

            if not data:
                raise CommandError("The feed returned no data.")

            fd, temp_name = tempfile.mkstemp(prefix="rpcompare_feed_", suffix=".csv")
            os.close(fd)
            with open(temp_name, "wb") as feed_file:
                feed_file.write(data)

            self.stdout.write("Importing products...")
            created, updated, offers_created, offers_updated = import_products(temp_name)

            self.stdout.write(self.style.SUCCESS(
                "Done. Products created: %s | updated: %s | offers created: %s | offers updated: %s"
                % (created, updated, offers_created, offers_updated)
            ))
        except CommandError:
            raise
        except Exception as exc:
            raise CommandError("Remote feed sync failed: %s" % exc)
        finally:
            if temp_name and os.path.exists(temp_name):
                try:
                    os.remove(temp_name)
                except OSError:
                    pass
