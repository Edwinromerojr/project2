from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWacthlist/<int:id>", views.removeWacthlist, name="removeWacthlist"),
    path("addWacthlist/<int:id>", views.addWacthlist, name="addWacthlist"),
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("addBidding/<int:id>", views.addBidding, name="addBidding"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction")
]
