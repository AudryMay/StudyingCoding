from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("create_comment", views.create_comment, name="create_comment"),
    path("create_bid", views.create_bid, name="create_bid"),
    path("end_listing", views.end_listing, name="end_listing"),
    path("watch_listing", views.watch_listing, name="watch_listing"),
    path("see_categories", views.see_categories, name="see_categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path(
        "go_to_category/<str:categoryName>", views.go_to_category, name="go_to_category"
    ),
    path("listing_page/<str:list_title>", views.listing_page, name="listing_page"),
]
