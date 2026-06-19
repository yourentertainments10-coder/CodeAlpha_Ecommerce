from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Product


IMAGE_URLS = {
    "hp-15s-laptop": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&h=675&q=85",
    "dell-inspiron-laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&h=675&q=85",
    "samsung-galaxy-m35": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&h=675&q=85",
    "redmi-note-14": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&h=675&q=85",
    "boat-rockerz-550": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&h=675&q=85",
    "noise-smart-watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&h=675&q=85",
    "mi-power-bank": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=900&h=675&q=85",
    "logitech-mouse": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&h=675&q=85",
    "hp-laptop-bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&h=675&q=85",
    "portronics-usb-hub": "https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=900&h=675&q=85",
    "cosmic-byte-keyboard": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&h=675&q=85",
    "redgear-mouse": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=900&h=675&q=85",
    "ant-esports-headset": "https://images.unsplash.com/photo-1599669454699-248893623440?auto=format&fit=crop&w=900&h=675&q=85",
    "levis-jacket": "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=900&h=675&q=85",
    "puma-shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&h=675&q=85",
    "allen-solly-shirt": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=900&h=675&q=85",
    "python-crash-course": "https://placehold.co/900x675/1f2937/f9fafb/png?text=Python+Crash+Course",
    "data-science-book": "https://placehold.co/900x675/0f766e/f9fafb/png?text=Data+Science+for+Beginners",
    "atomic-habits": "https://placehold.co/900x675/7c2d12/f9fafb/png?text=Atomic+Habits",
    "rich-dad-poor-dad": "https://placehold.co/900x675/78350f/f9fafb/png?text=Rich+Dad+Poor+Dad",
}

FALLBACK_IMAGE_URL = "https://placehold.co/900x675/111827/e5e7eb/png?text=Product+Image"


SAMPLE_PRODUCTS = [
   
("HP 15s Laptop", "Electronics", "15.6-inch laptop with Intel Core i5 processor, 8GB RAM and 512GB SSD.", "54999.00", 15, "hp-15s-laptop"),

("Dell Inspiron Laptop", "Electronics", "Dell Inspiron laptop with Full HD display and fast SSD storage.", "62999.00", 10, "dell-inspiron-laptop"),

("Samsung Galaxy M35", "Electronics", "5G smartphone with AMOLED display and 6000mAh battery.", "18999.00", 25, "samsung-galaxy-m35"),

("Redmi Note 14", "Electronics", "Redmi smartphone with powerful processor and 108MP camera.", "16999.00", 20, "redmi-note-14"),

("Boat Rockerz 550", "Electronics", "Wireless Bluetooth headphones with long battery backup.", "1999.00", 40, "boat-rockerz-550"),

("Noise Smart Watch", "Electronics", "Smart watch with heart-rate monitoring and fitness tracking.", "2499.00", 35, "noise-smart-watch"),

("Mi Power Bank 20000mAh", "Accessories", "Fast charging power bank with dual USB output.", "2299.00", 50, "mi-power-bank"),

("Logitech Wireless Mouse", "Accessories", "Ergonomic wireless mouse with silent clicks.", "899.00", 45, "logitech-mouse"),

("HP Laptop Bag", "Accessories", "Water-resistant laptop backpack with multiple compartments.", "1499.00", 30, "hp-laptop-bag"),

("Portronics USB Hub", "Accessories", "USB-C hub with HDMI and multiple USB ports.", "1299.00", 20, "portronics-usb-hub"),

("Cosmic Byte Mechanical Keyboard", "Gaming", "RGB mechanical gaming keyboard with blue switches.", "2499.00", 20, "cosmic-byte-keyboard"),

("Redgear Gaming Mouse", "Gaming", "RGB gaming mouse with adjustable DPI settings.", "799.00", 40, "redgear-mouse"),

("Ant Esports Gaming Headset", "Gaming", "Gaming headset with noise-cancelling microphone.", "1499.00", 25, "ant-esports-headset"),

("Levi's Denim Jacket", "Fashion", "Classic blue denim jacket for casual wear.", "3499.00", 15, "levis-jacket"),

("Puma Running Shoes", "Fashion", "Lightweight running shoes with cushioned sole.", "2999.00", 20, "puma-shoes"),

("Allen Solly Men's Shirt", "Fashion", "Cotton formal shirt suitable for office wear.", "1499.00", 30, "allen-solly-shirt"),

("Python Crash Course", "Books", "Beginner-friendly Python programming book.", "699.00", 25, "python-crash-course"),

("Data Science for Beginners", "Books", "Introduction to data analysis, visualization and machine learning.", "899.00", 20, "data-science-book"),

("Atomic Habits", "Books", "Popular self-improvement book by James Clear.", "499.00", 50, "atomic-habits"),

("Rich Dad Poor Dad", "Books", "Personal finance classic by Robert Kiyosaki.", "399.00", 45, "rich-dad-poor-dad"),

]


class Command(BaseCommand):
    help = "Seed the database with realistic sample products."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for name, category, description, price, stock, seed in SAMPLE_PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "price": Decimal(price),
                    "stock": stock,
                    "image_url": IMAGE_URLS.get(seed, FALLBACK_IMAGE_URL),

                },

            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded products complete: {created} created, {updated} updated."
            )
        )
