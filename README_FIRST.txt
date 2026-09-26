RPCOMPARE COMPLETE PROJECT

This is a complete fresh Django project. It includes manage.py, settings,
URLs, models, migrations, templates, CSS, sitemap, admin, affiliate
redirects, CSV importing and price history.

LOCAL SETUP
1. Open PowerShell in this folder.
2. Install Django 1.11.29:
   python -m pip install -r requirements.txt
3. Create the database:
   python manage.py migrate
4. Import the included products:
   python manage.py sync_products --file products.csv
5. Create an admin account if needed:
   python manage.py createsuperuser
6. Start:
   python manage.py runserver

PYTHONANYWHERE
The project already allows:
roshanp.pythonanywhere.com

Upload the whole project. Install requirements in the PythonAnywhere
virtualenv, run migrate, import products, run collectstatic, then reload
the web app.

AFFILIATE LINKS
affiliate_url is intentionally a field for REAL affiliate URLs from
merchant programs. The sample URLs are ordinary merchant URLs and do not
represent active affiliate tracking.

CONTACT / LEGAL
The contact, privacy and terms pages contain placeholders. Replace them
with your real contact information and finalized legal text before
publishing.

IMPORTANT
Do not delete the whole existing PythonAnywhere database if you want to
keep your existing 30-product data. This package is designed to be a
clean source-code starting point.


COMPATIBILITY FIX: This project uses Python 3.4-compatible string paths because the local environment is Python 3.4 and Django 1.11.29.
