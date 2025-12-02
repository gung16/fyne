import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fyne.settings')
django.setup()

from products.models import SkincareProduct
from django.contrib.auth.models import User

admin = User.objects.get(username='admin')

products = [
    {
        'name': 'Hydrating Essence Toner',
        'brand': 'COSRX',
        'category': 'toner',
        'ingredients': 'Hyaluronic Acid, Niacinamide, Panthenol',
        'description': 'Lightweight toner that provides deep hydration'
    },
    {
        'name': 'Niacinamide 10% + Zinc Serum',
        'brand': 'The Ordinary',
        'category': 'serum',
        'ingredients': 'Niacinamide, Zinc PCA',
        'description': 'High-strength vitamin and mineral serum'
    },
    {
        'name': 'UV Aqua Rich Watery Essence',
        'brand': 'Bioré',
        'category': 'sunscreen',
        'ingredients': 'Titanium Dioxide, Zinc Oxide, Hyaluronic Acid',
        'description': 'SPF 50+ PA++++ lightweight sunscreen'
    },
    {
        'name': 'Good Morning Low pH Cleanser',
        'brand': 'COSRX',
        'category': 'cleanser',
        'ingredients': 'Salicylic Acid, Tea Tree Oil, Betaine Salicylate',
        'description': 'Gentle gel cleanser with pH 5.0-6.0'
    },
    {
        'name': 'Advanced Snail Mucin Cream',
        'brand': 'COSRX',
        'category': 'moisturizer',
        'ingredients': 'Snail Mucin, Ceramides, Peptides',
        'description': 'Intense hydration and skin repair cream'
    }
]

created = []
for p in products:
    product = SkincareProduct.objects.create(
        name=p['name'],
        brand=p['brand'],
        category=p['category'],
        ingredients=p['ingredients'].split(', '),  # Convert to list for JSONField
        description=p['description']
    )
    created.append(product)
    print(f"Created: {p['name']}")

print(f"\nTotal created: {len(created)} products")
