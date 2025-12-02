from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SkincareProduct, ProductUsage, IngredientSafety
from datetime import date

@login_required
def product_list(request):
    """List all products and user's active products"""
    user_products = ProductUsage.objects.filter(user=request.user, end_date__isnull=True)
    all_products = SkincareProduct.objects.all()
    
    # Get list of product IDs that are in user's routine
    user_product_ids = list(user_products.values_list('product_id', flat=True))
    
    return render(request, 'products/product_list.html', {
        'user_products': user_products,
        'all_products': all_products,
        'user_product_ids': user_product_ids,
    })

@login_required
def product_detail(request, pk):
    """View product details and safety check"""
    product = get_object_or_404(SkincareProduct, pk=pk)
    
    # Check if user has safety check for this product
    safety_check = IngredientSafety.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    # Check if user is currently using this product
    usage = ProductUsage.objects.filter(
        user=request.user,
        product=product,
        end_date__isnull=True
    ).first()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'safety_check': safety_check,
        'usage': usage,
    })

@login_required
def add_product(request):
    """Add new product to catalog"""
    if request.method == 'POST':
        ingredients_str = request.POST.get('ingredients', '').strip()
        ingredients_list = [ing.strip() for ing in ingredients_str.split(',') if ing.strip()] if ingredients_str else []
        
        product = SkincareProduct.objects.create(
            name=request.POST.get('name'),
            brand=request.POST.get('brand'),
            category=request.POST.get('category'),
            ingredients=ingredients_list,
            description=request.POST.get('description', ''),
        )
        
        # Handle image upload if provided
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        messages.success(request, 'Product added successfully!')
        return redirect('products:product_detail', pk=product.pk)
    
    return render(request, 'products/add_product.html')

@login_required
def add_to_routine(request, pk):
    """Add product to user's routine"""
    product = get_object_or_404(SkincareProduct, pk=pk)
    
    if request.method == 'POST':
        ProductUsage.objects.create(
            user=request.user,
            product=product,
            frequency=request.POST.get('frequency', 'pm'),
            start_date=date.today(),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, f'{product.name} added to your routine!')
        return redirect('products:product_list')
    
    return render(request, 'products/add_to_routine.html', {'product': product})

@login_required
def ingredient_safety(request):
    """Check ingredient safety"""
    safety_checks = IngredientSafety.objects.filter(user=request.user)
    return render(request, 'products/ingredient_safety.html', {'safety_checks': safety_checks})

@login_required
def check_product_safety(request, pk):
    """Run safety check on a product"""
    product = get_object_or_404(SkincareProduct, pk=pk)
    
    # Simple safety logic (can be enhanced with AI/ML)
    risky_ingredients = ['alcohol', 'fragrance', 'parabens', 'sulfates']
    flagged = [ing for ing in product.ingredients if any(risky in ing.lower() for risky in risky_ingredients)]
    
    if flagged:
        risk_level = 'avoid' if len(flagged) > 2 else 'caution'
    else:
        risk_level = 'safe'
    
    safety, created = IngredientSafety.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            'risk_level': risk_level,
            'flagged_ingredients': flagged,
            'notes': f'Found {len(flagged)} potentially problematic ingredients.' if flagged else 'All ingredients appear safe for general use.'
        }
    )
    
    messages.success(request, 'Safety check completed!')
    return redirect('products:product_detail', pk=product.pk)
