from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse


# REGISTER VIEW
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    # ✅ FIX 1: correct template path
    return render(request, 'register.html')


# LOGIN VIEW
# supports redirecting back to the page the user originally requested
# if the user hit checkout (or any other protected view) while anonymous,
# the ?next= querystring will contain that path. after successful login we
# honour it, but if the target is the checkout page we instead send the
# visitor to the cart as requested by the feature spec.

def login_view(request):
    # capture both GET (initial link) and POST (when form submitted)
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # if user was heading for the checkout we return them to cart
            if next_url:
                if next_url.endswith('/checkout/') or next_url.endswith('/checkout'):
                    return redirect('cart')
                return redirect(next_url)
            return redirect('home')  # default landing page
        else:
            messages.error(request, 'Invalid username or password')
            # preserve next in case they try again
            if next_url:
                return redirect(f"{reverse('login')}?next={next_url}")
            return redirect('login')

    # ✅ FIX 2: correct template path
    # pass next along so the template can include it in the form
    context = {}
    if next_url:
        context['next'] = next_url
    return render(request, 'login.html', context)


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')
