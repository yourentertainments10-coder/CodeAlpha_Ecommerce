from django.conf import settings
from django.db import models


PRODUCT_IMAGE_FALLBACK_URL = "https://placehold.co/900x675/111827/e5e7eb/png?text=Product+Image"

PRODUCT_IMAGE_FALLBACKS = {
    "laptop": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&h=675&q=85",
    "smartphone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&h=675&q=85",
    "phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&h=675&q=85",
    "mouse": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&h=675&q=85",
    "book": "https://placehold.co/900x675/1f2937/f9fafb/png?text=Book+Cover",
    "books": "https://placehold.co/900x675/1f2937/f9fafb/png?text=Book+Cover",
    "fashion": "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=900&h=675&q=85",
    "shirt": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=900&h=675&q=85",
    "jacket": "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=900&h=675&q=85",
    "shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&h=675&q=85",
}


class Product(models.Model):
    class Meta:
        ordering = ["-created_at"]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def display_image_url(self) -> str:
        if self.image:
            return self.image.url

        if self.image_url:
            return self.image_url

        return self.display_image_fallback_url

    @property
    def display_image_fallback_url(self) -> str:
        image_key = f"{self.category} {self.name}".lower()

        for keyword, url in PRODUCT_IMAGE_FALLBACKS.items():
            if keyword in image_key:
                return url

        return PRODUCT_IMAGE_FALLBACK_URL


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart({self.user_id})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self) -> str:
        return f"CartItem(cart={self.cart_id}, product={self.product_id}, qty={self.quantity})"


class Order(models.Model):
    class Meta:
        ordering = ["-order_date"]

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELED = "CANCELED", "Canceled"

    class PaymentMethod(models.TextChoices):
        COD = "COD", "Cash on Delivery"
        UPI = "UPI", "UPI"
        NETBANKING = "NETBANKING", "Net Banking"
        CARD = "CARD", "Credit/Debit Card"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    order_date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"Order({self.id})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at purchase time

    def __str__(self) -> str:
        return f"OrderItem(order={self.order_id}, product={self.product_id}, qty={self.quantity})"

