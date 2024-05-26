from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Category, Listing, Comment, Bids

from datetime import date
import logging


def render_index_with_listings(request, listings, title):
    return render(
        request, "auctions/index.html", {"listings": listings, "title": title}
    )


def index(request):
    activeListings = Listing.objects.filter(is_active=True)
    return render_index_with_listings(request, activeListings, "Active Listings")


def watchlist(request):
    watchedListings = request.user.watchedListings.all()
    return render_index_with_listings(request, watchedListings, "Watched Listings")


def go_to_category(request, categoryName):
    activeListings = Listing.objects.filter(is_active=True)
    selectedCategory = activeListings.filter(category__categoryName=categoryName)
    return render_index_with_listings(request, selectedCategory, categoryName)


def see_categories(request):
    categories = Category.objects.values_list("categoryName", flat=True)
    print(type(categories))
    return render(request, "auctions/category_listing.html", {"categories": categories})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.values_list("categoryName", flat=True)
        return render(
            request, "auctions/create_listing.html", {"categories": categories}
        )

    else:
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]

        owner = request.user

        categoryName = request.POST["category"]
        category = Category.objects.get(categoryName=categoryName)
        newListing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            owner=owner,
        )

        newListing.save()

        return HttpResponseRedirect(reverse("index"))


def get_listing_from_id(listing_id):
    return Listing.objects.get(id=listing_id)


@login_required
def create_comment(request):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = get_listing_from_id(request.POST["listing_id"])
        commentor = request.user
        date_user_input = date.today()

        newComment = Comment(
            comment=comment,
            listing=listing,
            commentor=commentor,
            date=date_user_input,
        )

        newComment.save()
        listing_title = listing.title
        return HttpResponseRedirect(
            reverse("listing_page", kwargs={"list_title": listing_title})
        )


@login_required
def watch_listing(request):
    if request.method == "POST":
        listing = get_listing_from_id(request.POST["listing_id"])
        listing_title = listing.title

        if request.user in listing.usersWatching.all():
            listing.usersWatching.remove(request.user)
        else:
            listing.usersWatching.add(request.user)

        return HttpResponseRedirect(
            reverse("listing_page", kwargs={"list_title": listing_title})
        )


@login_required
def end_listing(request):
    if request.method == "POST":
        listing = get_listing_from_id(request.POST["listing_id"])
        listing_title = listing.title

        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(
            reverse("listing_page", kwargs={"list_title": listing_title})
        )


def listing_page(request, list_title):
    if request.method == "GET":
        listed_item = Listing.objects.get(title=list_title)
        return render(request, "auctions/listing_page.html", {"listing": listed_item})


@login_required
def create_bid(request):
    if request.method == "POST":
        new_bid = float(request.POST["new_bid"])
        listing = get_listing_from_id(request.POST["listing_id"])
        listing_title = listing.title

        min_price = listing.starting_bid

        if listing.bids.exists():
            min_price = listing.bids.first().bid

        if min_price >= new_bid:
            bid_message = "Bid must be higher than current highest"
            messages.error(request, bid_message, extra_tags="bid_message")
            return redirect(listing_page, list_title=listing_title)

        bid = Bids(bid=new_bid, listing=listing, bidder=request.user)
        bid.save()

        return HttpResponseRedirect(
            reverse("listing_page", kwargs={"list_title": listing_title})
        )
