from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import Listing, User, Bid

def index(request):
    listings = Listing.objects.all()
    if not listings:
        listings = []

    return render(request, "auctions/index.html", {
        "listings": listings
    })

def getListing(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/itemView.html", {
        "listing": listing
    })

def bid(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    success = True
        
    if request.method == "POST" and user:
        bid = float(request.POST["bid"])
        print(f"{user.username} placed a bid for", str(bid))
        # if bid > listing max bid, its the highest 
        if listing.max_bid < bid:
            # make bid object
            try:
                bid_object = Bid.objects.create(listing=listing, price=bid, user=user)
                bid_object.save()
                listing.max_bid = bid
                listing.save()
            except:
                print("Errored somehow")
                success = False
            # save user who placed the bid too
            

    return render(request, "auctions/itemView.html", {
        "listing": listing
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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
