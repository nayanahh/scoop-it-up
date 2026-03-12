from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Food

# ========================================
# HOME VIEW - Displays all food items
# ========================================
@login_required(login_url='login')  # Only logged-in users can access
def home(request):
    categories = Category.objects.all()
    foods = Food.objects.all()
    context = {
        'categories': categories,
        'foods': foods,
    }
    return render(request, 'home.html', context)

# ========================================
# OPTIONAL: Filter foods by category
# ========================================
@login_required(login_url='login')
def category_foods(request, category_id):
    categories = Category.objects.all()
    foods = Food.objects.filter(category_id=category_id)
    context = {
        'categories': categories,
        'foods': foods,
        'selected_category': category_id
    }
    return render(request, 'home.html', context)
