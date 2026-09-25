from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^search/$", views.search, name="search"),
    url(r"^product/(?P<slug>[-\w]+)/$", views.product_detail, name="product_detail"),
    url(r"^category/(?P<slug>[-\w]+)/$", views.category, name="category"),
    url(r"^about/$", views.about, name="about"),
    url(r"^contact/$", views.contact, name="contact"),
    url(r"^privacy/$", views.privacy, name="privacy"),
    url(r"^terms/$", views.terms, name="terms"),url(r"^go/(?P<offer_id>\d+)/$", views.go_to_offer, name="go_offer"),
    url(r"^stores/$", views.stores, name="stores"),
    url(
    r"^stores/(?P<store_id>[0-9]+)/$",
    views.store_detail,
    name="store_detail"
),
]
