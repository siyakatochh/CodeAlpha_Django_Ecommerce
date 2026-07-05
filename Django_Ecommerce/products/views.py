from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Product, Cart, Order, Wishlist


# ---------------- HOME ----------------
def home(request):
    category = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if query:
        products = products.filter(name__icontains=query)

    cart_count = Cart.objects.count()

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0

    return render(request, "home.html", {
        "products": products,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


# ---------------- LOGOUT ----------------
def user_logout(request):
    logout(request)
    return redirect('home')


# ---------------- CART ----------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart')


# ---------------- CHECKOUT ----------------
@login_required
def checkout(request):
    cart_items = Cart.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                total=item.product.price * item.quantity
            )

        Cart.objects.all().delete()

        return render(request, "success.html")

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })


# ---------------- MY ORDERS ----------------
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "orders.html", {
        "orders": orders
    })


# ---------------- WISHLIST ----------------
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(request, "wishlist.html", {
        "wishlist_items": wishlist_items
    })


@login_required
def remove_wishlist(request, wishlist_id):
    item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')
  
# ---------------- PRODUCT DETAILS ----------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "product_detail.html", {
        "product": product
    })

# ---------------- ABOUT ----------------
def about(request):
    return render(request, "about.html")


# ---------------- CONTACT ----------------
def contact(request):
    return render(request, "contact.html")