from __future__ import print_function

import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Run the configured RPCompare remote-feed synchronization."

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Download timeout in seconds."
        )

    def handle(self, *args, **options):
        feeds = os.environ.get("RPCOMPARE_FEEDS", "").strip()
        if not feeds:
            raise CommandError(
                "RPCOMPARE_FEEDS is not configured. "
                "Set it to StoreName=https://feed.csv;Store2=https://feed2.csv"
            )

        self.stdout.write("Starting scheduled RPCompare feed sync...")

        call_command(
            "sync_remote_feeds",
            timeout=options.get("timeout") or 60
        )

        self.stdout.write(
            self.style.SUCCESS("Scheduled RPCompare feed sync finished.")
        )
