from django.shortcuts import render, redirect, HttpResponse
from .models import *
from shop.forms import CustomCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from django.db import transaction


def home(request):
    products = Products.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourites.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    else:
        return redirect("/")


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect("/")


def remove_cart(request, cid):
    cartitems = Cart.objects.get(id=cid)
    cartitems.delete()
    return redirect("/cart")


def remove_fav(request, fid):
    favitems = Favourites.objects.get(id=fid)
    favitems.delete()
    return redirect("/favviewpage")


def fav_page(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        if request.user.is_authenticated:
            data = json.load(request)
            products_id = data["pid"]
            # print(request.user.id)
            product_status = Products.objects.get(id=products_id)
            if product_status:
                if Favourites.objects.filter(
                    user=request.user.id, products_id=products_id
                ):
                    return JsonResponse(
                        {"status": "product already in Favourite"}, status=200
                    )
                else:
                    Favourites.objects.create(
                        user=request.user, products_id=products_id
                    )
                    return JsonResponse(
                        {"status": "Product sucessfully added to favourite"}, status=200
                    )
        else:
            return JsonResponse({"status": "Login to add Favourite"}, status=200)
    else:
        return JsonResponse({"status": "Invalid Access"}, status=200)


def add_to_cart(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data["product_qty"]
            product_id = data["pid"]
            # print(request.user.id)
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse(
                        {"status": "Product Already in Cart"}, status=200
                    )
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user,
                            product_id=product_id,
                            product_qty=product_qty,
                        )
                        return JsonResponse(
                            {"status": "Product Added to Cart"}, status=200
                        )
                    else:
                        return JsonResponse(
                            {"status": "Product Stock Not Available"}, status=200
                        )
        else:
            return JsonResponse({"status": "Login to Add Cart"}, status=200)
    else:
        return JsonResponse({"status": "Invalid Access"}, status=200)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been Sucessfully logged in")
                return redirect("/")
            else:
                messages.error(request, "Invaid Username or Password")
                return redirect("/login")
        return render(request, "shop/login.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "User Logged Out Sucessfully")
    return redirect("/")


def register(request):
    form = CustomCreationForm()
    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Sucessful. You Can Login Now")
            return redirect("/login")
    return render(request, "shop/register.html", {"form": form})


def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})


def collectionview(request, name):
    if Category.objects.filter(status=0, name=name):
        products = Products.objects.filter(category__name=name)
        return render(
            request,
            "shop/products/index.html",
            {"products": products, "category_name": name},
        )
    else:
        messages.warning(request, "no such category found")
        return redirect("collections")


def productdetails(request, cname, pname):
    if Category.objects.filter(name=cname, status=0):
        if Products.objects.filter(name=pname, status=0):
            products = Products.objects.filter(name=pname, status=0).first()
            return render(
                request, "shop/products/product_details.html", {"products": products}
            )
        else:
            messages.warning(request, "no such product found")
            return redirect("collections")

    else:
        messages.warning(request, "no such category found")
        return redirect("collections")
