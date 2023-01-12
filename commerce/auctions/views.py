from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bidding, Bid


def index(request):
    #active Listing
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#create listing
def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        # Who is the user
        currentUser = request.user
        #ValueError at /create Cannot assign "'shirt'": "Listing.category" must be a "Category" instance.
        # Get all content about the particular category
        categoryData = Category.objects.get(categoryName=category)
        # create a bid object
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        # Create a new listing object
        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=bid,
            category=categoryData,
            owner=currentUser
        )
        # Insert the object in our database
        newListing.save()
        # Redirect to index page
        return HttpResponseRedirect(reverse(index))

#Display Categories
def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories
        })
    
#listing page
def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    #for comments 2
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Bidding.objects.filter(listing=listingData)
    #close action
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments":allComments,
        "isOwner": isOwner
    })

#Watchlist
def removeWacthlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWacthlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
#Comment
def addBidding(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newBid']

    newBid = Bidding(
        author=currentUser,
        listing=listingData,
        message=message
    )
    newBid.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

#Bidding
def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    #sample2
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Bidding.objects.filter(listing=listingData)
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing":listingData,
            "message": "Bid was updated successfully",
            "update":True,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments":allComments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing":listingData,
            "message": "Bid updated failed",
            "update":False,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments":allComments
        })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Your auction is closed."
    })