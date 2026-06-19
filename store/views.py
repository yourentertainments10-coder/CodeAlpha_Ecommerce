from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from .models import Cart, CartItem, Order, OrderItem, Product


UserModel = get_user_model()


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def home(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    categories = ["Electronics", "Accessories", "Gaming", "Fashion", "Books"]
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    if query:
        products = products.filter(name__icontains=query)

    if selected_category:
        products = products.filter(category__iexact=selected_category)

    return render(
        request,
        "home.html",
        {
            "products": products,
            "categories": categories,
            "query": query,
            "selected_category": selected_category,
        },
    )



def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    base_products = Product.objects.exclude(pk=product.pk)
    related_products = base_products.filter(category=product.category)[:4] if product.category else Product.objects.none()
    similar_products = base_products.exclude(pk__in=related_products.values("pk"))[:4]

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "similar_products": similar_products,
        },
    )


def cart_detail(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")

    cart = _get_or_create_cart(request.user)
    items = list(cart.items.select_related("product").all())
    subtotal = Decimal("0")

    for item in items:
        item.line_total = item.product.price * item.quantity
        subtotal += item.line_total

    delivery_charge = Decimal("0.00")
    tax_amount = Decimal("0.00")
    grand_total = subtotal + delivery_charge + tax_amount

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "tax_amount": tax_amount,
            "grand_total": grand_total,
        },
    )


@login_required(login_url="login")
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("product_detail", pk=product_id)


    product = get_object_or_404(Product, pk=product_id)
    cart = _get_or_create_cart(request.user)

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("cart_detail")

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        # New cart item should start at quantity=1
        cart_item.quantity = 1
    else:
        cart_item.quantity = min(cart_item.quantity + 1, product.stock)

    cart_item.save(update_fields=["quantity"])

    return redirect("cart_detail")


@login_required(login_url="login")
def cart_update(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_or_create_cart(request.user)

    new_qty = int(request.POST.get("quantity", "1"))
    new_qty = max(1, new_qty)
    new_qty = min(new_qty, product.stock if product.stock > 0 else 0)

    if new_qty <= 0:
        CartItem.objects.filter(cart=cart, product=product).delete()
        return redirect("cart_detail")

    CartItem.objects.update_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": new_qty},
    )
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("cart_detail")

    product = get_object_or_404(Product, pk=product_id)
    cart = _get_or_create_cart(request.user)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect("cart_detail")


@login_required(login_url="login")
def checkout(request: HttpRequest) -> HttpResponse:
    cart = _get_or_create_cart(request.user)
    items = list(cart.items.select_related("product").all())

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    # Totals (simple: subtotal + fixed delivery)
    subtotal = Decimal("0")
    for item in items:
        product = item.product
        if product.stock < item.quantity:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect("cart_detail")
        subtotal += product.price * item.quantity

    delivery_fee = Decimal("0")
    total = subtotal + delivery_fee

    return render(
        request,
        "checkout.html",
        {
            "items": items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total": total,
        },
    )


@login_required(login_url="login")
def payment_select(request: HttpRequest) -> HttpResponse:
    cart = _get_or_create_cart(request.user)
    items = list(cart.items.select_related("product").all())

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    subtotal = Decimal("0")
    for item in items:
        product = item.product
        if product.stock < item.quantity:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect("cart_detail")
        subtotal += product.price * item.quantity

    delivery_fee = Decimal("0")
    total = subtotal + delivery_fee

    if request.method != "POST":
        return render(
            request,
            "payment_selection.html",
            {
                "items": items,
                "subtotal": subtotal,
                "delivery_fee": delivery_fee,
                "total": total,
            },
        )

    payment_method = request.POST.get("payment_method")

    if payment_method != "COD":
        # Do not create order for unfinished payment methods
        messages.info(
            request,
            "Payment integration is currently under development. Please use Cash on Delivery.",
        )
        return render(request, "payment_unavailable.html")

    # COD: create order
    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status=Order.Status.PENDING,
            payment_method=payment_method,
        )

        for item in items:
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price,
            )
            Product.objects.filter(pk=product.pk).update(stock=F("stock") - item.quantity)

        cart.items.all().delete()

    return render(request, "order_confirmation.html", {"order": order})



@login_required(login_url="login")
def order_history(request: HttpRequest) -> HttpResponse:
    orders = request.user.orders.prefetch_related("items__product").all()
    return render(request, "order_history.html", {"orders": orders})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if UserModel.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "register.html")

        user = UserModel.objects.create_user(username=email, email=email, password=password, first_name=name)
        login(request, user)
        return redirect("home")

    return render(request, "register.html")


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials.")

    return render(request, "login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")

