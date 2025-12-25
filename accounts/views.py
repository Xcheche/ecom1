from django.shortcuts import render

# Create your views here.


def about(request):
    return render(request, "accounts/about.html")


def register(request):
    return render(request, "accounts/signup.html")


def login(request):
    return render(request, "accounts/login.html")


def dashboard(request):
    return render(request, "accounts/dashboard.html")
