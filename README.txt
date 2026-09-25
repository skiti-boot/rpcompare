RPcompare
=========
Price comparison website built for Django 1.11.29 / Python 3.4.

Run:
1. python manage.py migrate
2. python manage.py createsuperuser
3. python manage.py runserver

Then open http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

Before public deployment:
- change SECRET_KEY
- set DEBUG=False
- configure ALLOWED_HOSTS
- configure production static files
- add real retailer/affiliate integrations
- publish complete Privacy/Terms pages
