from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "index.html", context=None)

def login(request):
    return render(request, "login.html", context=None)
