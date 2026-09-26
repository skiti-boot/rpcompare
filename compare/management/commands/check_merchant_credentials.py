from __future__ import print_function
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Check whether required merchant credential environment variables are present."

    def handle(self, *args, **options):
        groups = {
            "Amazon": [
                "AMAZON_CREATOR_CLIENT_ID",
                "AMAZON_CREATOR_CLIENT_SECRET",
                "AMAZON_PARTNER_TAG",
            ],
            "eBay": [
                "EBAY_CLIENT_ID",
                "EBAY_CLIENT_SECRET",
            ],
        }
        optional = ["EBAY_CAMPAIGN_ID", "EBAY_REFERENCE_ID"]
        all_ok = True
        for merchant, variables in groups.items():
            self.stdout.write("\n%s" % merchant)
            for variable in variables:
                present = bool(os.environ.get(variable))
                status = "OK" if present else "MISSING"
                self.stdout.write("  %-35s %s" % (variable, status))
                if not present:
                    all_ok = False
        self.stdout.write("\nOptional eBay settings")
        for variable in optional:
            status = "SET" if os.environ.get(variable) else "NOT SET"
            self.stdout.write("  %-35s %s" % (variable, status))
        if all_ok:
            self.stdout.write(self.style.SUCCESS("\nRequired merchant credentials are present."))
        else:
            self.stdout.write(self.style.WARNING("\nSome required credentials are missing. This check does not test whether credentials are valid."))
