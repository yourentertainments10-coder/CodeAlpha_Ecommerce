from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Product


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
                    # Prefer online image URLs for easy seeding
                    # Map slugs to product-specific online images.
                    "image_url": {
                        "hp-15s-laptop": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80",
                        "dell-inspiron-laptop": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
                        "samsung-galaxy-m35": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80",
                        "redmi-note-14": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=900&q=80",
                        "boat-rockerz-550": "https://images.unsplash.com/photo-1518441902112-a8f0a1b6f3d8?auto=format&fit=crop&w=900&q=80",
                        "noise-smart-watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
                        "mi-power-bank": "https://images.unsplash.com/photo-1587613999984-2d4f1a5a1f0f?auto=format&fit=crop&w=900&q=80",
                        "logitech-mouse": "https://images.unsplash.com/photo-1555617952-4f45e7b2b4a4?auto=format&fit=crop&w=900&q=80",
                        "hp-laptop-bag": "https://images.unsplash.com/photo-1526481280695-3c687fd5432c?auto=format&fit=crop&w=900&q=80",
                        "portronics-usb-hub": "https://images.unsplash.com/photo-1587825140708-dfafb8a1b2f5?auto=format&fit=crop&w=900&q=80",
                        "cosmic-byte-keyboard": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
                        "redgear-mouse": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80",
                        "ant-esports-headset": "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=900&q=80",
                        "levis-jacket": "https://images.unsplash.com/photo-1520975916090-3105956dac38?auto=format&fit=crop&w=900&q=80",
                        "puma-shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
                        "allen-solly-shirt": "https://images.unsplash.com/photo-1520975661595-6453be3f7070?auto=format&fit=crop&w=900&q=80",
                        "python-crash-course": "https://images.unsplash.com/photo-1517423440428-a5a00ad493e8?auto=format&fit=crop&w=900&q=80",
                        "data-science-book": "https://images.unsplash.com/photo-1455885666463-62d9b1d369f2?auto=format&fit=crop&w=900&q=80",
                        "atomic-habits": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=900&q=80",
                        "rich-dad-poor-dad": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=900&q=80",
                    }.get(seed, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"),

                },

            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded products complete: {created} created, {updated} updated."
            )
        )
