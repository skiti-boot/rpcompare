from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from compare.sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
}

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django_sitemap",
    ),
    url(r"^", include("compare.urls")),
]

# Serve project static files during local development and on PythonAnywhere while DEBUG=True.
urlpatterns += staticfiles_urlpatterns()
